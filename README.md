# Contributor License Agreement (CLA) Registry

This repository serves as a simple **registry of approved contributors** who are allowed to contribute to our projects.
Only users who have their **hashed GitHub username** stored here are permitted to submit contributions.

The repository does **not** store any personal data — only anonymous, irreversible **SHA-256 hashes**.

---

## 📝 How to Become an Approved Contributor

1. Generate a SHA-256 hash of your GitHub username (guide below).
2. Create a **pull request** to this repository.
3. Add your hash to `contributors.json` or `contributors.txt`.
4. After your PR is approved, you are authorized to contribute to our projects.

---

## 🔐 How to Generate a SHA-256 Hash

### 🔹 Windows (PowerShell – works on any Windows 10/11)

```powershell
[Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes("GitHubUsername"))).ToLower()
```

### 🔹 Windows (short version, if you have OpenSSL)

```powershell
echo -n "GitHubUsername" | openssl sha256
```

---

### 🔹 Linux / macOS (terminal)

```sh
echo -n "GitHubUsername" | sha256sum | awk '{ print $1 }'
```

---

## 📁 File Structure

### `contributors.json`

```json
{
  "contributors": [
    "f4c3b5678c9a1e23d4...",
    "7bc9123ea4f9d8..."
  ]
}
```

### `contributors.txt`

```
f4c3b5678c9a1e23d4...
7bc9123ea4f9d8...
```

---

## 🤖 How the System Verifies CLA Approval

Our tools or GitHub Actions:

1. retrieve the committer’s GitHub username,
2. generate the SHA-256 hash,
3. compare it with the hashes stored in this repository,
4. if it matches → **CLA is valid**.

### ✅ Automatic Pull Request Verification

The `Verify Contributor Hash` workflow runs on every pull request to `main` that modifies `contributors.json` or `contributors.txt`.

It will:

* obtain the GitHub username of the PR author,
* generate a SHA-256 hash from it,
* verify that all newly added entries in the contributor lists match this hash.

If the hash does not match, the GitHub Action fails and the pull request cannot be merged until the correct value is provided.

---

## 🛡️ Privacy Protection

We do **not** store:

* real names
* e-mail addresses
* GitHub profile links
* any other identifying data

Only anonymous SHA-256 hashes.
