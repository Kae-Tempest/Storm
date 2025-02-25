import logging
import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.propagate import extract
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("opentelemetry")
# Initialisation du traceur et du propagateur
tracer = trace.get_tracer(__name__)
propagator = TraceContextTextMapPropagator()


def configure_opentelemetry(service_name="Storm"):
    """Configure OpenTelemetry with OTLP exporter."""

    # Configuration du Resource avec les métadonnées de votre service
    resource = Resource.create({"service.name": service_name})

    # Configuration du TracerProvider avec notre Resource
    trace_provider = TracerProvider(resource=resource)
    # Configuration de l'exporteur OTLP HTTP
    # Modifiez l'URL selon votre configuration
    try:
        otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
        timeout = 10
        otlp_exporter = OTLPSpanExporter(
            endpoint=otlp_endpoint,
            timeout=timeout,
            insecure=True,
            credentials=None
        )
        # Ajout au TracerProvider
        trace_provider.add_span_processor(BatchSpanProcessor(
            span_exporter=otlp_exporter,
            # Configuration plus agressive du batch pour éviter les pertes
            max_export_batch_size=512,
            schedule_delay_millis=5000,  # 5 secondes
            max_queue_size=2048,
        ))

        logger.info("Exporteur OTLP configuré avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de la configuration de l'exporteur OTLP: {e}")
        logger.warning("Utilisation uniquement de l'exporteur console")

    # Définition du TracerProvider global
    trace.set_tracer_provider(trace_provider)

    # 6. Instrumentation des frameworks
    try:
        DjangoInstrumentor().instrument()
        logger.info("Instrumentation de Django réussie")
    except Exception as e:
        logger.error(f"Erreur lors de l'instrumentation de Django: {e}")

    try:
        RequestsInstrumentor().instrument()
        logger.info("Instrumentation de Requests réussie")
    except Exception as e:
        logger.error(f"Erreur lors de l'instrumentation de Requests: {e}")

    # 9. Instrumentation PostgreSQL avec psycopg3
    PsycopgInstrumentor().instrument(enable_commenter=True)
    logger.info("Instrumentation de PostgreSQL (psycopg3) réussie")

    # 10. Instrumentation des logs
    try:
        LoggingInstrumentor().instrument(set_logging_format=True)
        logger.info("Instrumentation des logs réussie")
    except Exception as e:
        logger.error(f"Erreur lors de l'instrumentation des logs: {e}")

    # 10. Instrumentation spécifique à Django PostgreSQL (optionnel)
    try:
        from django.db import connection

        db_engine = connection.settings_dict['ENGINE']
        db_name = connection.settings_dict['NAME']
        db_host = connection.settings_dict['HOST']

        logger.info(f"Base de données configurée: {db_engine} - {db_name} sur {db_host}")
    except Exception as e:
        logger.warning(f"Impossible de récupérer les infos de la base de données: {e}")

    return trace_provider


# Ajout du middleware pour la propagation du contexte
class OpenTelemetryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifiez si la requête est destinée à l'API ninja
        if request.path.startswith('/api/'):  # Ajustez selon votre préfixe d'API
            # Extraction du contexte de trace des en-têtes
            carrier = {}
            for header_name, header_value in request.headers.items():
                carrier[header_name] = header_value

            context = extract(carrier)

            with tracer.start_as_current_span(
                    f"{request.method} {request.path}",
                    context=context,
                    kind=trace.SpanKind.SERVER
            ) as span:
                span.set_attribute("http.method", request.method)
                span.set_attribute("http.url", request.build_absolute_uri())
                span.set_attribute("http.route", request.path)

                # Exécuter la requête
                response = self.get_response(request)

                span.set_attribute("http.status_code", response.status_code)
                return response

        # Pour les requêtes non-API, simplement passer au middleware suivant
        return self.get_response(request)
