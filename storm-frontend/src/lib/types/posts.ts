export interface Posts {
    id: number;
    content: string;
    likes_count: number;
    is_liked: boolean;
    created_at: string;
    author: {
        id: number;
        username: string;
    };
}