# Reviewer notes

- Factual gate: no production implementation, permission grant, or API
  support is established by this request.
- Whole document: can a contributor distinguish the current problem, chosen
  proposal, alternative and observable outcome without reading an API note?
- Japanese prose: remove the repeated consequence if it makes the introduction
  circular, but do not compress the proposal into a string of nouns.

## One possible rewrite

### 課題

GitHub Actions でイメージを公開していますが、[Docker Hub の説明文](https://hub.docker.com/r/aoirint/ffmpeg)
を変更するには、Docker Hub の画面で別途編集する必要があります。

### 提案

説明文をリポジトリ内の Markdown ファイルで管理し、変更を GitHub Actions から Docker Hub に反映する。

### 代替案

リリース手順に、Docker Hub で説明文を手動更新する作業を追加する。

### 完了条件

GitHub に取り込んだ説明文の変更が、Docker Hub の画面を操作しなくても公開ページに反映される。
