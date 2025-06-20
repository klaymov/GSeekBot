from __future__ import annotations

import re
import html
from uuid import uuid4
from urllib.parse import unquote, parse_qs

from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from bot.services import duckduckgo

router = Router()


@router.inline_query()
async def inline_result(
    query: InlineQuery,
):
    if not query.query or query.query == ' ':
        return
    
    results = []
    search_results = await duckduckgo.get(query.query)
    
    if not search_results:
        return
    
    for item in search_results:
        body = item.get('body', '').strip()
        href = item.get('href', '').strip()
        title = item.get('title', '').strip()
        
        if 'duckduckgo.com/l/?' in href:
            query_params = parse_qs(href.split('?', 1)[1])
            if 'uddg' in query_params:
                href = unquote(query_params['uddg'][0])
        
        if not body and not href and not title:
            continue
    
        step1 = re.sub(r'\s*\[[^\]]*?\]\s*', ' ', body)
        _body = re.sub(r' {2,}', ' ', step1).strip()
        escaped_href = html.escape(href, quote=True)
        url_symbol = f'<a href="{escaped_href}">→</a>'
        message_text = _body.replace(' ...', '…')+' '+url_symbol
        
        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=title or _body[:30],
                input_message_content=InputTextMessageContent(
                    message_text=message_text,
                    disable_web_page_preview=True
                ),
                url=href,
                hide_url=True,
                description=_body[:200]
            )
        )
    
    await query.answer(results=results)
