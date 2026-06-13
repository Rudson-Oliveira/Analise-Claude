"""Ferramentas de agendamento/publicação (scheduler)."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..client import MetricoolClient, safe_call

# Documentação compartilhada da estrutura do post.
_POST_SHAPE = """
Estrutura do objeto `info` (JSON):
    text: Texto do post.
    providers: lista com ao menos um provedor, ex.: [{"network": "instagram"}].
               Use "twitter" para o X.
    publicationDate: {"dateTime": "2025-01-01T10:00:00", "timezone": "America/Sao_Paulo"}.
                     Use o timezone obtido em get_brands.
    media: lista de URLs de mídia (normalize antes com normalize_media_url). Padrão [].
    mediaAltText: lista de textos alternativos. Padrão [].
    autoPublish: True/False (padrão True).
    draft: True/False (padrão False).
    firstCommentText: texto do primeiro comentário (padrão "").
    shortener: True/False (padrão False).
    smartLinkData: {"ids": []}.
    Inclua o *networkData* APENAS das redes presentes em providers (vazio se não
    houver detalhes). Formatos:
        twitterData:   {"tags": []}            # tags = marcações em imagens, não hashtags
        facebookData:  {"boost": 0, "boostPayer": "", "boostBeneficiary": "", "type": "", "title": ""}
        instagramData: {"autoPublish": True, "tags": []}
        linkedinData:  {"documentTitle": "", "publishImagesAsPDF": False, "previewIncluded": True, "type": "", "poll": {}}
        pinterestData: {"boardId": "", "pinTitle": "", "pinLink": "", "pinNewFormat": True}
        youtubeData:   {"title": "", "type": "", "privacy": "", "tags": [], "category": "", "madeForKids": False}
        tiktokData:    {"disableComment": False, "disableDuet": False, "disableStitch": False, "privacyOption": "", "title": "", "autoAddMusic": False}
        blueskyData:   {"postLanguages": []}
        threadsData:   {"allowedCountryCodes": []}

Requisitos por rede: Instagram/TikTok exigem ao menos 1 imagem ou vídeo;
Pinterest exige imagem + boardId; YouTube exige vídeo + título + madeForKids;
Facebook Reel exige vídeo; Facebook Story exige imagem ou vídeo.
A data NÃO pode estar no passado.
"""


def register(mcp: FastMCP, client: MetricoolClient) -> None:
    @mcp.tool()
    async def schedule_post(blog_id: int, info: dict) -> Any:
        """Agenda (ou publica) um post no Metricool.

        Se o usuário não informar o horário, use get_best_time_to_post.
        Se faltar mídia/título obrigatório para a rede, pergunte ao usuário antes
        de enviar.

        Args:
            blog_id: blogId da marca (obtido em get_brands).
            info: Objeto JSON do post (ver estrutura abaixo).
        """
        return await safe_call(
            client.post("/v2/scheduler/posts", params={"blogId": blog_id}, json_body=info)
        )

    schedule_post.__doc__ = (schedule_post.__doc__ or "") + _POST_SHAPE

    @mcp.tool()
    async def update_scheduled_post(post_id: str, blog_id: int, info: dict) -> Any:
        """Atualiza um post agendado. Requer o id (obtido em get_scheduled_posts).

        Confirme com o usuário, descrevendo o que será alterado, antes de enviar.
        Não refaça automaticamente em caso de erro. Envie o conteúdo COMPLETO do
        post original, alterando apenas os campos desejados e preservando a
        estrutura. Inclua "id" e "uuid" do post dentro de `info`.

        Args:
            post_id: id do post a atualizar.
            blog_id: blogId da marca (obtido em get_brands).
            info: Objeto JSON completo do post com as alterações.
        """
        return await safe_call(
            client.put(
                f"/v2/scheduler/posts/{post_id}",
                params={"blogId": blog_id},
                json_body=info,
            )
        )

    @mcp.tool()
    async def get_scheduled_posts(
        blog_id: int,
        init_date: str,
        end_date: str,
        timezone: str | None = None,
    ) -> Any:
        """Lista os posts agendados de uma marca em um período.

        Use o ``id``/``uuid`` retornado para editar (update_scheduled_post) ou
        excluir (delete_scheduled_post).

        Args:
            blog_id: blogId da marca (obtido em get_brands).
            init_date: Data inicial no formato 2025-01-01.
            end_date: Data final no formato 2025-01-01.
            timezone: Timezone da marca (opcional), ex.: "America/Sao_Paulo".
        """
        params = {
            "blogId": blog_id,
            "start": f"{init_date}T00:00:00",
            "end": f"{end_date}T23:59:59",
            "timezone": timezone,
        }
        return await safe_call(client.get("/v2/scheduler/posts", params=params))

    @mcp.tool()
    async def delete_scheduled_post(post_id: str, blog_id: int) -> Any:
        """Exclui um post agendado pelo id. Operação destrutiva — confirme antes.

        Args:
            post_id: id do post (obtido em get_scheduled_posts).
            blog_id: blogId da marca (obtido em get_brands).
        """
        return await safe_call(
            client.delete(f"/v2/scheduler/posts/{post_id}", params={"blogId": blog_id})
        )
