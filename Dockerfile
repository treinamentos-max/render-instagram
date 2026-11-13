FROM alpine:3.21

# Python + Pillow + Chromium + emoji + fontconfig (tudo do mesmo repositorio, sem pip)
RUN apk add --no-cache python3 py3-pillow chromium font-noto-emoji fontconfig

# Fonte da marca (Poppins)
COPY fonts/ /usr/share/fonts/poppins/
RUN fc-cache -f

WORKDIR /app
COPY server.py templates.py /app/
COPY assets/ /app/assets/

ENV PORT=8080 DATA_DIR=/data RETENTION_HOURS=72 CHROME_BIN=/usr/bin/chromium
VOLUME /data
EXPOSE 8080
CMD ["python3", "/app/server.py"]
