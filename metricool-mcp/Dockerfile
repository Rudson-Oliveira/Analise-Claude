FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir .

# stdio por padrão; sobrescreva com METRICOOL_MCP_TRANSPORT para HTTP/SSE.
ENV METRICOOL_MCP_TRANSPORT=stdio

ENTRYPOINT ["metricool-mcp"]
