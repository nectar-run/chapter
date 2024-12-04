<!-- PROJECT LOGO -->
<p align="center">
  <a href="https://github.com/chapter-gtm/chapter">
   <img src="https://github.com/chapter-gtm/chapter/blob/main/assets/images/github-cover.png" alt="Logo">
  </a>

  <h3 align="center">Chapter</h3>

  <p align="center">
    The open-source GTM tool for developer tools.
    <br />
    <a href="https://chapter.show"><strong>Learn more »</strong></a>
    <br />
    <a href="https://github.com/chapter-gtm/chapter/issues">Issues</a>
    <br />
    <a href="https://cal.com/robing/open-source-gtm">Talk to founders</a>
    <br />
  </p>

<br />

</p>

> [!IMPORTANT]
> Chapter is under active development, and is currently in public beta. This repository is updated regularly with new features and overall improvements.

<br />
Chapter is the 1st open source GTM tool designed for developer tool companies. We beleive that developer tools need a new kind of sales tool when selling to mid-market and enterprise. One that requires zero click or manual work AND provides a broad combination of niche data points that you can trust to have high confidence that a lead is relevant. Only that way can you trust that a lead is relevant to your business and can reach out in a geniune way. The future is relevancy.

## About the Project

<img width="100%" alt="booking-screen" src="https://github.com/chapter-gtm/chapter/blob/main/assets/images/github-chapter-screenshots.png">

# Chapter - Lead research, purpose-built for developer tools

It takes 1 minute to create an AI agent that researches for relevant leads matching your exact search criteria around the clock. Get daily leads in real-time based on a wide variety of triggers, and evidence on why they matter.

### Built With

- [Next.js](https://nextjs.org/?ref=chapter.show)
- [React.js](https://reactjs.org/?ref=chapter.show)
- [Tailwind CSS](https://tailwindcss.com/?ref=chapter.show)
- [shadcn/ui](https://ui.shadcn.com/?ref=chapter.show)
- [Tiptap](https://tiptap.dev/?ref=chapter.show)
- [Litestar](https://litestar.dev)
- [SQLAlchemy](https://sqlalchemy.org/?ref=chapter.show)
- [PostgreSQL](https://postgresql.org/?ref=chapter.show)

## Quick Start

To quickly get a development environment running, run the following:

```shell
make install
. .venv/bin/activate
```

### Local Development

```bash
cp .env.local.example .env
pdm run start-infra # this starts a database and redis instance only
# this will start the SAQ worker, Vite development process, and Litestar
pdm run app run

# to stop the database and redis, run
pdm run stop-infra
```

### Docker

```bash
docker compose up
```

Note: This project integrates with third-party APIs. You will need to obtain the necessary API keys for these services and update them in your `.env` file. For example, see the provided `.env.docker.example` file for the required format.
