# Investigation comment: Docker Hub description updates

## Editor packet

Revise these sections of an investigation comment for maintainers considering
how to automate Docker Hub description updates. Write in Japanese. Keep the
helpful sources; this is a research reply, not an implementation proposal.

The opening below is an actual excerpt from an earlier public revision of
[the investigation comment](https://github.com/aoirint/ffmpeg-docker/issues/96#issuecomment-7064148965).
The second excerpt is from a later public revision. The comment is editable;
the link may show newer wording.

```text
[Docker の公式ガイド](https://docs.docker.com/build/ci/github-actions/update-dockerhub-desc/)では、イメージを公開するステップとは別に、サードパーティ製の `peter-evans/dockerhub-description` を使って説明文を更新しています。[docker/build-push-action #21](https://github.com/docker/build-push-action/issues/21) でも、説明文の更新は Buildx とは別の Action で扱う方針が示されています。Issue は Close されています。

[Docker Hub の公開 API リファレンス](https://docs.docker.com/reference/api/hub/latest/)には、既存リポジトリの Overview を更新する操作が載っていません。[公開 API の対応を求める Issue](https://github.com/docker/hub-feedback/issues/2392) が開かれています。
```

```text
`/v2/repositories/{namespace}/{repository}` は、[Docker Hub の API 変更履歴ページ](https://docs.docker.com/reference/api/hub/changelog/#2025-09-19)によると、2025 年 9 月 19 日に `/v2/namespaces/{namespace}/repositories/{repository}` が追加された際に、リポジトリの情報を取得する `GET` メソッドと、存在を確認する `HEAD` メソッドを提供するエンドポイントとして非推奨となったことが確認できましたが、リポジトリの説明文を変更する `PATCH` メソッドについての記載はありませんでした。また同時に、リポジトリ作成用の `POST /v2/repositories` と `POST /v2/repositories/{namespace}` も非推奨化されていました。
```

Context: the [2022 OpenAPI definition](https://github.com/docker/docs/blob/3883cac81719610e478808dcba2d579893dcdf70/docker-hub/api/latest.yaml#L823-L865)
described the legacy description PATCH; an [August 2022 docs commit](https://github.com/docker/docs/commit/f930f14d635c53a521e3e8befb7eb99ead3e6016)
removed that definition. The September 2025 changelog entry concerns GET,
HEAD, and repository-creation POSTs, not the description PATCH. The publication
status of the operation does not establish its current runtime behavior.
