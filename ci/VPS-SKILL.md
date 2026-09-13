---
name: singbox-vps-deploy
description: Safely deploy or maintain sing-box on a Linux VPS, especially Alpine containers with very low memory, using VLESS Reality with XTLS Vision and optionally publishing Clash or raw VLESS subscriptions. Also append client outbounds (AnyTLS / Clash Meta) to an existing box without replacing current nodes.
---

# Sing-box VPS Deploy

Deploy a working node, not merely a running process. Preserve unrelated services and existing subscription entries.

## Authorization and secrets

- Inspect first: OS/architecture, cgroup memory and swap limits, disk, listeners, firewall, current services, and NAT/port-forwarding.
- Do not uninstall, stop, replace, or repurpose an existing node unless the user explicitly asks. “Update the subscription” means **add a new entry by default**, not replace an old one.
- Never persist passwords, UUIDs, Reality private keys, import URIs, subscription URLs, or host-specific IPs in this skill or memory.
- Do not echo passwords or private keys. A VLESS import URI and QR may be returned only in the private task response.
- Generate QR codes locally/offline. Never send an import URI to a public QR service.

## Port contract

1. Check occupied ports and the provider's external-to-internal mappings.
2. Let the selected installer generate or suggest a random available port first.
3. Show that port and pause for the user's final port choice when it has not already been supplied.
4. Recheck the chosen final port immediately before binding it.

Do not silently choose a final port. If the VPS is behind NAT, the service must listen on the mapped internal port unless the provider mapping is changed by the user.

## Workflow

1. Audit the exact installer source the user selected. Download it to a file, record its SHA-256, syntax-check it, and inspect network fetches, service changes, firewall changes, credential changes, and uninstall paths before execution.
2. Use the user's chosen protocol and script. For this workflow the expected server contract is VLESS + REALITY + TCP + `xtls-rprx-vision`; do not substitute another protocol without approval.
3. On low-memory Alpine containers, including 64–96 MiB cgroup limits, read [references/alpine-low-memory.md](references/alpine-low-memory.md) before installing.
4. Validate the generated configuration with `sing-box check`, then verify the init service is started, enabled at boot, and listening on the final port. After a management-panel port reset, compare the live config, generated URI, and any `.config_cache`; some scripts update the listener but leave the initial random port cached.
5. Restrict the configuration directory to `0700` and files containing UUIDs, Reality keys, passwords, or import URIs to `0600`; do not accept installer defaults of `0644` for these files.
6. Test the public TCP mapping from a different machine.
7. Run an actual client through the node and make an HTTPS request. Record the observed exit IP/country and TLS success. A listener or systemd/OpenRC status alone is not proof.
8. If subscription publishing is authorized, read [references/subscription-publishing.md](references/subscription-publishing.md). Use `scripts/add_subscription_node.py` for compatible static Clash/raw files; it produces new files and never overwrites inputs.
9. Generate a local QR and provide concise import instructions. Do not disclose the Reality private key.

## Add outbound / subscription node

This is a different job from deploying a new inbound.

When the user pastes a client profile (AnyTLS, VLESS, Trojan, Shadowrocket/Stash JSON, Clash YAML) and says add it / 加上去 / 追加节点:

1. Treat it as an **outbound append**. Do not deploy a new VLESS+REALITY inbound unless they explicitly asked to stand up a server.
2. Add one new entry. Do not replace, reorder, or delete existing outbounds, proxies, inbounds, or unrelated services. If a selector / urltest / `proxy-groups` list already exists and they asked to use the new node, attach the new tag to that list only.
3. Never write passwords, UUIDs, subscription URLs, or host IPs into this skill, memory, git, or Drive skill files.
4. Identify the live stack before editing:
   - `sing-box` → `outbounds` in the live `config.json`
   - `mihomo` / Clash Meta → `proxies:` in the live YAML
   Inspect process list and common paths (`/etc/sing-box`, `/usr/local/etc/sing-box`, `~/.config/sing-box`, `/etc/mihomo`, `/etc/clash`) if unknown.
5. Copy a timestamped backup of the live config. Patch only after the backup exists.
6. Field mapping for client exports:
   - AnyTLS auth field is `password`. Ignore leftover `uuid` unless the protocol actually uses it.
   - Ignore `peer: 127.0.0.1` from local client dumps.
   - `tlsProfile` / `client-fingerprint` maps to uTLS fingerprint (often `chrome`).
   - Set `insecure` / `skip-cert-verify` only if the paste has `allowInsecure: 1`.
7. Validate, then reload:
   - sing-box: `sing-box check -c <file>` then restart/reload the service
   - mihomo: config test then reload
8. Do not claim success without a client HTTPS request through the new tag.

### Agent reachability

Grok / cloud agents often have no SSH connector and cannot route to RFC1918 addresses. If the target is LAN-only, or there is no key/jump host in this session:

- Do not pretend the node was added.
- Give a paste-ready outbound snippet and a one-shot command for the operator to run on that host.
- Do not encode that host's IP, username, or credentials as universal policy.

### sing-box outbound template

Fill from the user's paste. Do not store the filled values in this file.

```json
{
  "type": "anytls",
  "tag": "<name>",
  "server": "<host>",
  "server_port": 0,
  "password": "<password>",
  "tls": {
    "enabled": true,
    "server_name": "<host>",
    "insecure": false,
    "utls": {
      "enabled": true,
      "fingerprint": "chrome"
    }
  }
}
```

### mihomo / Clash Meta template

```yaml
- name: <name>
  type: anytls
  server: <host>
  port: 0
  password: <password>
  client-fingerprint: chrome
  udp: true
  skip-cert-verify: false
```

## Add subscription provider

When the user says only add the subscription / 只加订阅:

- Append a Clash Meta `proxy-providers` HTTP entry. Do not replace the live client YAML with the subscription document (those documents often include mixed-port, rules, and controller settings).
- Request the provider with a Clash Meta User-Agent. A generic UA may return placeholder nodes instead of AnyTLS.
- Attach the provider to an existing select/urltest group with `use:`. Do not wipe existing `proxies`.
- Original sing-box without a provider module cannot ingest a Clash HTTP subscription; convert selected nodes to outbounds or use mihomo.
- Never write the subscription URL or token into this skill.

## Failure handling

- Do not repeat an OOM-producing package installation unchanged. Inspect `memory.events`, remove only identified temporary artifacts, then use the bounded low-memory path.
- Preserve successful earlier nodes/configs when a later step fails. Leave a timestamped rollback copy before publishing.
- Stop if the requested forwarded port is unavailable, the external mapping is absent, configuration validation fails, or end-to-end proxying cannot be proven.
- Do not claim success from a health check that did not traverse the new VLESS outbound or the newly added outbound tag.

## Maintenance

The user has authorized maintaining this skill. After a real deployment exposes a reusable failure mode, update the smallest relevant instruction or helper, run `quick_validate.py`, and exercise the changed behavior with a secret-free fixture. Do not encode one host's credentials, endpoints, or accidental quirks as universal policy.
