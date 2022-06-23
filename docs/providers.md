# Providers

> Provider - site offering disposable phone numbers as a public service

The following providers are supported by disposable-phonebook:

{% for provider in dphonebook_providers %}

- {{ provider.domain() }}

{% endfor %}


## Enabling / disabling providers

Not all providers are enabled by default. To set a list of enabled providers,
specify `enabled_providers:list` config option in the configuration file:

```yaml
enabled_providers:
  - dummy.example.com
  - sms-online.co
```

The values are domain names of the providers.
