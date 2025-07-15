from schemas.content import ContentGenerationRequest

def generate_mock_content(request: ContentGenerationRequest) -> dict:
    """
    This function simulates content generation based on the provided request.
    It returns a mock response that mimics the structure of a real content generation service.
    """
    print(f"Generating content for: '{request.topic}' on {request.platforms}")

    mock_response = {}
    if "blog" in request.platforms:
        mock_response["blog"] = f"Fake blog post: A deep analysis of '{request.topic}'."
    if "twitter" in request.platforms:
        mock_response["twitter"] = f"Fake tweet: Quick thoughts on '{request.topic}'. #Mock"
    if "instagram" in request.platforms:
        mock_response["instagram"] = f"Fake Instagram post: Visual inspiration for '{request.topic}'. 📸✨"

    return mock_response