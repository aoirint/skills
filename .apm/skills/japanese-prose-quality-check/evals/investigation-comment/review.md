# Review: Investigation comment

Use these notes to compare whole drafts. A concise draft can still be harder to
read if it turns source labels into subjects or removes the transitions that
show why the next finding matters.

## Structure and prose

- **Opening and headings.** The report starts with what was investigated and
  when. The time dates the observations; it is not an edit timestamp.
  Name what each section tells the reader. A request-payload heading is too
  narrow for a section on permissions or the behavior of an Action.
- **A sequence with a point.** The proposal, maintainer response, and observed
  recommendation form one account of how the project handles the update.
  The closing date alone does not explain that outcome. The guide introduces a
  procedure; the implementation carries it out. Choose the verb accordingly.
- **A connected explanation.** The create/update contrast gives the reason to
  look beyond the current reference. The user report then gives a concrete
  method, and the maintainer response qualifies that method. Keep them as
  separate attributed observations without dropping the bridge between them.
  A short transition such as 「このエンドポイントについて」 carries a known
  topic forward; a new topic such as authentication needs its own lead-in.
- **A comparison the reader can follow.** Name the exact method and path,
  including the historical trailing slash. A documented PATCH disappearing
  from an OpenAPI definition is not a service removal, and a later GET/HEAD
  deprecation does not cover PATCH. In a historical comparison, give the
  commit or date when it helps the reader follow which source changed.
  Keep source names and labels consistent; put references by the passage
  they support.

## Notes outside the scoring scope

- If extending the case beyond its excerpts, introduce the operation before
  its authentication. Keep the maintainer
  explanation, reported outcomes and a particular implementation's
  recommendation distinct. Do not infer a universal token requirement from
  them, attribute a difference to age without evidence, or switch to a
  credential type outside the task. Keep actual implications, not a catalogue
  of unrelated caveats.

## Observed revisions

These are visible differences between drafts and the published comment.
The notes identify what the wording does, not why every edit was made.

- 「更新しています」 in a sentence about the guide became
  「更新する手順が紹介されています」. This makes the guide's role explicit
  without claiming it performs the update.
- An isolated 「Issue は Close されています。」 became part of the account
  that starts with the proposal, attributes the maintainer's decision to a
  reply, and contrasts the outcome with what the official guide shows.
- The short 「公開 API リファレンスには…更新する操作が載っていません」 was
  replaced by the creation-versus-update contrast. The next two paragraphs
  distinguish the user report of an actual update from the maintainer's
  statement about that endpoint.
- An early title 「Action が送るリクエスト」 was replaced as the report's
  structure changed. The finished comment has distinct sections on the API,
  CI permissions, and third-party Action implementation; authentication
  details no longer open the report.
- A later draft traces the definition and the Repositories introduction
  separately. The PATCH definition disappeared in August 2022, the
  introduction initially stayed, and the introduction changed in November
  2023. The dates belong to different edits, not to service retirement.
  For the March 2022 commit, the wording moved from 「追加されました」 to
  「追加されていました」. The point is not the ending itself: it makes an
  obscure fact read as something found in the investigation, rather than
  background the reader was expected to know.

## Published excerpts

The [public investigation comment](https://github.com/aoirint/ffmpeg-docker/issues/96#issuecomment-7064148965)
contains these passages. They are transcribed as published, not a newly
written answer. Each fenced selection is contiguous; omitted intervening
material includes other findings, authentication and permissions.

```text
### Docker 公式リポジトリにおける上流 Issue

2020 年 3 月、Docker Hub の説明文もイメージと一緒に更新できるようにする提案が、[docker/build-push-action](https://github.com/docker/build-push-action) の Issue #21 として起票されています。この Issue への返信で、メンテナーは 2023 年に、説明文の更新機能は [docker/build-push-action](https://github.com/docker/build-push-action) へは組み込まず、別の Action で扱う方針を示しています。この方針が示された後、Issue は 2024 年 3 月に Close されています。しかし、Docker 公式の専用 Action が公開されたことは確認できず、2026 年 11 月 21 日時点の公式ガイドでは、サードパーティ製の [peter-evans/dockerhub-description](https://github.com/peter-evans/dockerhub-description) を使って説明文を更新する手順が紹介されています。

- https://github.com/docker/build-push-action/issues/21
- https://docs.docker.com/build/ci/github-actions/update-dockerhub-desc/
```

```text
### 説明文の更新に関する Docker Hub API の仕様

Docker Hub の公開 API リファレンスには、新規リポジトリの作成時に説明文を指定する方法の記載はありましたが、既存リポジトリの説明文を更新する操作に関する記載はありませんでした。

- https://docs.docker.com/reference/api/hub/latest/
- https://docs.docker.com/reference/api/hub/latest/schemas/repo_creation_request/

一方、2023 年に reitzig さんが [docker/hub-feedback](https://github.com/docker/hub-feedback) の [Issue #2127 へのコメント](https://github.com/docker/hub-feedback/issues/2127#issuecomment-1616804120)で、説明文を更新できたと報告しています。報告の例では、公開リファレンスに記載されていない `PATCH /v2/repositories/{namespace}/{repository}/` に JSON を送り、Overview の Markdown を `full_description` に、短い説明文を `description` に指定しています。

- https://github.com/docker/hub-feedback/issues/2127#issuecomment-1616804120

このエンドポイントについて、Docker のメンテナーは 2023 年に同リポジトリの [Issue #2321 へのコメント](https://github.com/docker/hub-feedback/issues/2321#issuecomment-1509700957)で、`/v2/repositories/...` 形式のエンドポイントを `legacy endpoints` と呼んでおり、このエンドポイントを使用した説明文の更新には、リポジトリの管理権限が必要であるとしています。

- https://github.com/docker/hub-feedback/issues/2321#issuecomment-1509700957
```

```text
`/v2/repositories/{namespace}/{repository}` は、[Docker Hub の API 変更履歴ページ](https://docs.docker.com/reference/api/hub/changelog/#2025-09-19)によると、2025 年 9 月 19 日に `/v2/namespaces/{namespace}/repositories/{repository}` が追加された際に、リポジトリの情報を取得する `GET` メソッドと、存在を確認する `HEAD` メソッドを提供するエンドポイントとして非推奨となったことが確認できましたが、リポジトリの説明文を変更する `PATCH` メソッドについての記載はありませんでした。また同時に、リポジトリ作成用の `POST /v2/repositories` と `POST /v2/repositories/{namespace}` も非推奨化されていました。

- https://docs.docker.com/reference/api/hub/changelog/#2025-09-19
- https://docs.docker.com/reference/api/hub/deprecated/
```

```text
[docker/docs](https://github.com/docker/docs) によると、2022 年 8 月 26 日 01:13 JST のコミット [`f930f14d`](https://github.com/docker/docs/commit/f930f14d635c53a521e3e8befb7eb99ead3e6016) で削除されるまで、OpenAPI 定義において `/v2/repositories/{namespace}/{repository}/` の `PATCH` メソッドは `PatchRepositoryDescription` として定義されており、リクエストの `full_description` には Markdown を指定できると記載されていました。

- https://github.com/docker/docs/blob/3883cac81719610e478808dcba2d579893dcdf70/docker-hub/api/latest.yaml#L823-L865
- https://github.com/docker/docs/blob/3883cac81719610e478808dcba2d579893dcdf70/docker-hub/api/latest.yaml#L2000-L2024
- https://github.com/docker/docs/commit/f930f14d635c53a521e3e8befb7eb99ead3e6016
```

```text
2022 年 3 月 10 日（JST）のコミット [`117dfca0`](https://github.com/docker/docs/commit/117dfca0fc5d9ff08c46fbd1742e331ddda58ef4) では、Docker Hub API v2 リファレンスの Repositories 節に「リポジトリの説明文などの設定を管理できる」という案内が、説明文を更新する `PATCH` メソッドの定義とともに追加されていました。同年 8 月 26 日（JST）のコミット [`f930f14d`](https://github.com/docker/docs/commit/f930f14d635c53a521e3e8befb7eb99ead3e6016) では、タグ一覧や個別のタグを取得する `GET` と、タグの存在を確認する `HEAD` の定義が追加され、説明文を更新する `PATCH` メソッドの定義が削除されていました。一方、Repositories 節の案内はそのまま残っていました。2023 年 11 月 18 日（JST）のコミット [`2da43407`](https://github.com/docker/docs/commit/2da43407ace2b19b5bcbd10c7f188ddf8d9f0cdd) では、同節の案内が、調査時点のコミット [`747e4c75`](https://github.com/docker/docs/commit/747e4c7528c703b357b1ae83cbbf411229ce59d2) と同じ「リポジトリのタグを参照できる」という記述に書き換えられていました。

- https://github.com/docker/docs/commit/117dfca0fc5d9ff08c46fbd1742e331ddda58ef4
- https://github.com/docker/docs/blob/f930f14d635c53a521e3e8befb7eb99ead3e6016/docker-hub/api/latest.yaml#L98-L102
- https://github.com/docker/docs/commit/2da43407ace2b19b5bcbd10c7f188ddf8d9f0cdd
- https://github.com/docker/docs/blob/747e4c7528c703b357b1ae83cbbf411229ce59d2/content/reference/api/hub/latest.yaml#L128-L132
```
