import uuid

from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from aiogram_i18n import I18nContext
from dishka.integrations.aiogram import FromDishka

from app.gseekbot.core.services.search_aggregator import SearchAggregatorService

router = Router()


@router.inline_query()
async def inline_search(
    query: InlineQuery,
    i18n: I18nContext,
    search_aggregator: FromDishka[SearchAggregatorService],
):
    text = query.query.strip()
    if not text:
        return await query.answer([], cache_time=1)

    results_data = await search_aggregator.aggregate(text)
    
    ai_answer = results_data["ai"]
    google_answers = results_data["google"]

    inline_results = []
    
    # 1. AI Result
    ai_result = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title=i18n.inline.ai_title(),
        description=ai_answer,
        thumbnail_url="https://www.androidsage.com/wp-content/uploads/2025/07/Google-Gemini-New-Logo.jpg",
        input_message_content=InputTextMessageContent(
            message_text=ai_answer
        )
    )
    inline_results.append(ai_result)

    # 2. Google Results
    for idx, g_res in enumerate(google_answers):
        g_title = g_res.get("title", f"Result {idx}")
        g_desc = g_res.get("description", "")
        g_thumb = g_res.get("favicon_url")
        
        inline_results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=g_title,
                description=g_desc,
                thumbnail_url=g_thumb,
                input_message_content=InputTextMessageContent(
                    message_text=g_desc
                )
            )
        )

    await query.answer(inline_results, cache_time=300)
