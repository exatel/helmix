Helmix
======
A simple Kubernetes templating engine, that:

- Is simpler than Helm and has simple dependencies. Goes well with k3s.
- Single python file, pip-installable if useful. Useful for air-gapped
  environments.
- Templates are simple and conscise (jinja2), but the validation is done by the
  kubectl during apply.
- Handles both templates of kubernetes files and application configs.
- Doesn't depend on a particular file structure or file formats.
- Experimental: Handles variable files encrypted with GPG.

Rationale
---------
There are multiple available solutions to this problem. Many people are probably
happy with a verbose Kustomize, and the rest is probably happily using Helm so
there's not much available 'simple' (yet good) solutions. I've tried: ktmpl
(nice but no configmaps), k8comp (config file, installation via docker/helm, no
configmaps), kustomize (verbose, configmaps but... not parametrized?), but they
didn't fit with my usecase.

Solution like this is so simple to write that I assume some companies might be
using similar self-made solutions internally, or they are so unpopular that I
wasn't able to find it.

Writing it took less time than initial research, publishing took another three
hours. Bonus features will probably take another 3h.

Examples
--------
Helmix doesn't assume any particular file structure. Example you could use:

    templates/
      base.yaml      (eg. namespaces)
      databases.yaml (some stateful sets)
      app.yaml       (some deployment)
    configs/
      app.conf.json  (application config in any format)
    envs/
      common.yaml    (common variables)
      test.yaml      (overrides for test environment)
      preprod.yaml   (overrides for preprod env)
      prod.yaml

Variables can be combined from multiple files to override only necessary
variables and keep the configuration DRY.

Render a single or multiple templates:

    helmix -v envs/common.yaml -v envs/test.yaml templates/*

Output can be piped to the kubectl, or you can pass `--apply` (and potentially
`--kubectl` and `--context`).

Generate a config map from a file, while applying template variables. This works
similarly to `kubectl create configmap app-config
--from-file=configs/app.conf.json`:

    helmix --apply --config-map app-config \
        -v envs/common.yaml -v envs/test1.yaml configs/app.conf.json

Inspect final variables, after combining:

    helmix -v envs/common.yaml -v envs/test1.yaml --dump


Options
-------
    usage: helmix [-h] [-v vars.yaml] [--dump] [-n NAMESPACE] [--config-map CONFIG_MAP]
                  [--apply] [--kubectl KUBECTL] [--context CONTEXT] [TEMPLATE ...]

    Simple k8s config generator

    positional arguments:
      TEMPLATE              template files to build

    optional arguments:
      -h, --help            show this help message and exit
      -v vars.yaml, --vars vars.yaml
                            paths to variable files in order
      --dump                dump final variables

    Config maps:
      -n NAMESPACE, --namespace NAMESPACE
                            namespace for configmap
      --config-map CONFIG_MAP
                            Name of the configmap to generate from a template

    Instant apply:
      --apply               instead of printing the template, apply it using kubectl
      --kubectl KUBECTL     path to the kubectl binary, by default uses $PATH
      --context CONTEXT     kubectl context to use, by default 'default'


Notes and TODOs
---------------
Note:
- Template code has to be trusted as it can execute arbitrary python
  code during rendering.

Possible todos:
- Allow vars to be a directory of files.
- Optional variable validation using a separate schema yaml.
- Merging lists variables should append instead of overriding?
  Could be defined in schema file along the validation.
