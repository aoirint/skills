# Review: Feature request

- **Title and opening.** The title states the requested outcome. The body can
  start with the concrete obstacle instead of repeating the title or adding
  that stale information may stay stale.
- **Shape of the issue.** The project's headings distinguish the current
  problem, proposed change, manual alternative, and observable outcome.
  Retain the local structure; do not turn it into a universal template.
- **Completion is not a task list.** The last section describes the public
  result. The creator's description does not need a maintainer progress
  checkbox, an implementation plan or reservations about API credentials.
- **Readable parallel sections.** Use direct verbs for the proposal and
  alternative. The outcome can stand as a sentence without
  「確認できれば完了です」 repeating the heading.

## Observed revisions

- The intermediate opening about old information was replaced by the
  concrete manual editing step. The published body does not repeat that
  forgetting an update leaves stale text.
- The problem and success criterion were separated into four sections.
  The manual path is an alternative, not another standing caveat in the
  problem statement.
- The first version of the completion criterion used a checkbox. The
  published version states the same outcome as ordinary prose.

## Published excerpt

The following is the body of [the public issue](https://github.com/aoirint/ffmpeg-docker/issues/96)
with the disclosure banner omitted. The issue title has since changed, while
the editor packet keeps the earlier title for its comparison.

```text
## 課題

GitHub Actions でイメージを公開していますが、[Docker Hub の説明文（Overview）](https://hub.docker.com/r/aoirint/ffmpeg) を変更するには、Docker Hub の画面で別途編集する必要があります。

## 提案

説明文をリポジトリ内の Markdown ファイルで管理し、その変更を GitHub Actions から Docker Hub に反映する。

## 代替案

リリース手順に、Docker Hub で説明文を手動更新する作業を追加する。

## 完了条件

GitHub に取り込んだ説明文の変更が、Docker Hub の画面を操作しなくても公開 Overview に反映される。
```
