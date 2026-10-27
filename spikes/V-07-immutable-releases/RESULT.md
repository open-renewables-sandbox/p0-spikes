# V-07 Immutable releases and Cloudflare Pages: result (Cloudflare part partial)

Date: 2026-10-27. Labels: **[Test]** observed here, **[Doc]** vendor documentation. Script: `run.sh`; run output is quoted below. Repository: `open-renewables-sandbox/p0-spikes` (public, free organisation).

## Outcome

**Immutable releases work on a free organisation's public repository.** After enabling the setting, a published release could no longer take, replace or lose an asset, its tag could no longer be moved or deleted, and its tag name could not be reused. Two things were not blocked: the release notes could still be edited, and the release itself could be deleted. The Cloudflare half is only partly answered from documentation.

## Immutable releases **[Test]**

Enabling: `PUT /repos/{owner}/{repo}/immutable-releases` returned `{"enabled":true,"enforced_by_owner":false}`; before, `GET` returned `enabled:false`. Test release `v0.0.3-p0`: created as a **draft** with one asset, then published (`gh release edit --draft=false`); the API then showed `"immutable": true`.

| Action after publishing | Result |
| --- | --- |
| Upload a new asset | refused: `HTTP 422: Cannot upload assets to an immutable release` |
| Replace the asset (`--clobber`) | refused: `Cannot delete asset from an immutable release` |
| Delete the asset | refused: same message |
| Move the tag (force push to another commit) | refused: `push declined due to repository rule violations` |
| Delete the tag | refused: same |
| Edit the release notes | **allowed** (the command succeeded) |
| Delete the release | **allowed**; the tag stayed on the remote |
| Create a new release on the same tag name | refused: `tag_name was used by an immutable release` |

Assets must therefore go up with creation or while the release is a draft. The W-07 flow is compatible: a one-step `gh release create v0.0.4-p0 --generate-notes <asset>` (no draft step) also produced `"draft":false,"immutable":true` with its asset attached **[Test]**. The release notes remain editable, so the notes are not the citable artefact; the tag and the assets are.

The setting is per repository here (`enforced_by_owner:false`). A tag that was ever used by an immutable release cannot be used again even after the release is deleted.

## Cloudflare Pages access policy **[Doc, partial]**

- Cloudflare's Pages documentation says an access policy can restrict viewing of **preview deployments** to the owner's account ("Enable access policy" in the project's settings), that other members need a multi-user account, and that it covers previews only, not the `*.pages.dev` production domain or custom domains.
- The pages I could read give **no statement of free-plan availability and no seat or user limit**. The Zero Trust account-limits page lists 500 Access applications and 500 reusable policies without splitting them by plan, and a limit of 50 custom Application Library applications on Zero Trust Free.
- A test needs a Cloudflare account and an API token kept outside the repository. **Not run; needs the owner.**

## Feeds

C-10 and AD-15's "immutable where the plan allows" are confirmed for public repositories on Free. SDD §11's "immutable where available (V-07)" for private libraries on Free is **not answered**: the sandbox repository is public. **P-6 is not triggered** by the GitHub part; the Cloudflare option (alpha or beta preview for a private library) stays unconfirmed.
