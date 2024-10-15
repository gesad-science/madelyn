# syntax=docker/dockerfile:1

FROM golang:1.23

WORKDIR /app

COPY . ./

RUN <<EOF
  go mod download
EOF

RUN CGO_ENABLE=0 GOOS=linux go build -o /madelyn-login-api cmd/main.go

EXPOSE 8000

ENTRYPOINT ["/madelyn-login-api"]

