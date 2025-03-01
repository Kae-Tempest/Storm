export interface Posts {
	id: number;
	content: string;
	likes_count: number;
	media_url: string;
	is_liked: boolean;
	created_at: string;
	location: string;
	privacy_settings: string;
	number_of_shares: number;
	author: {
		id: number;
		username: string;
	};
}

export interface CreatePost {
	content: string;
	media_url?: Blob | null;
	privacy_setting: string;
}