class Models:
    GPT_LATEST = "~openai/gpt-latest"
    GEMINI_LATEST = "~google/gemini-pro-latest"
    GEMINI_FLASH_LITE = "google/gemini-2.5-flash-lite"
    # [gpt-5.6-luna] gpt-5.6-luna-* 는 둘다 가격이 저렴하게 같고 성능이 뛰어남 컨텍스트 창도 넒음
    # gpt-5.6-luna-pro 는 추론 능력이 좋지만 느림
    GPT_LUNA_PRO = "openai/gpt-5.6-luna-pro"
    # gpt-5.6-luna 는 추론이 안좋지만 빠름
    GPT_LUNA = "openai/gpt-5.6-luna"
