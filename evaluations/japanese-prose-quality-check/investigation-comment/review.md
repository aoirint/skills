# Reviewer notes

- Factual gate: the guide introduces a procedure; the Action performs the
  update. Distinguish the 2022 removal from the specification from the 2025
  deprecation of other operations. Do not infer that the service removed PATCH.
- Whole section: does the opening explain the available approach before
  discussing the API? Can the reader locate and grasp the difference between
  the current documentation and the historical operation?
- Japanese prose: look for a natural introduction of the guide, sentences
  that carry the same topic forward, and manageable contrast. Do not reward a
  dense sentence merely because every clause is technically true.

## One possible rewrite

Docker の公式ガイドでは、イメージの公開とは別のステップで、
サードパーティ製の `peter-evans/dockerhub-description` を使って説明文を更新する手順が紹介されています。
Buildx にこの機能を組み込まず、別の Action で扱う方針は Issue #21 にも示されています。

- [Docker の公式ガイド](https://docs.docker.com/build/ci/github-actions/update-dockerhub-desc/)
- [docker/build-push-action の Issue #21](https://github.com/docker/build-push-action/issues/21)

既存リポジトリの説明文を更新する操作は、現在の公開 API リファレンスには載っていません。
旧 OpenAPI 定義には `PATCH /v2/repositories/{namespace}/{repository}/` がありましたが、
2022 年 8 月に定義から削除されました。
一方、2025 年 9 月の変更履歴が非推奨としたのは、同じパスの `GET` と `HEAD` などで、
説明文を更新する `PATCH` は挙げられていません。

- [現在の API リファレンス](https://docs.docker.com/reference/api/hub/latest/)
- [旧 OpenAPI 定義](https://github.com/docker/docs/blob/3883cac81719610e478808dcba2d579893dcdf70/docker-hub/api/latest.yaml#L823-L865)
- [定義を削除したコミット](https://github.com/docker/docs/commit/f930f14d635c53a521e3e8befb7eb99ead3e6016)
- [2025 年 9 月の API 変更履歴](https://docs.docker.com/reference/api/hub/changelog/#2025-09-19)
