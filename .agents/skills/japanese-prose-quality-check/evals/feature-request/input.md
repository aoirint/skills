# Feature request: Automating a Docker Hub description

## Editor packet

Rewrite the following Japanese feature request for maintainers. Give
contributors enough context to understand the proposed work, not the
implementation investigation. Keep the title.

Title: Docker Hub の説明文更新を自動化したい

The following is a reconstruction of an intermediate draft of
[the public issue](https://github.com/aoirint/ffmpeg-docker/issues/96);
it is not presented as a verbatim quote.

> Docker Hub に古い情報が残っています。GitHub Actions でイメージを公開していますが、説明文は連動して更新されません。
> 説明文を変えるたびに Docker Hub で別途編集する必要があり、更新が漏れると公開ページに古い情報が残ります。
> 更新手段や権限の調査も必要です。公開後の確認も行います。

Source facts: the image workflow publishes images but does not update the
[Docker Hub description](https://hub.docker.com/r/aoirint/ffmpeg). Changes to
the description are made separately in Docker Hub. The proposed change is to
manage it as Markdown in GitHub and have GitHub Actions publish revisions.
The manual alternative is to add that step to the release procedure. Success
means the public description reflects an accepted revision without operating
the Docker Hub UI. The local issue format uses 課題, 提案, 代替案, and 完了条件
with the completion condition written as a sentence.
