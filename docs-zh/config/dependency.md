# 项目依赖

-----

[项目依赖项](metadata.md#dependencies) 使用 [PEP 508][] 字符串定义的可选的 [PEP 440 version specifiers][] 。

## 版本说明符

版本说明符由一系列用逗号分隔的版本子句组成。例如：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project]
    ...
    dependencies = [
      "cryptography",
      "click>=7, <9, != 8.0.0",
      "python-dateutil==2.8.*",
      "numpy~=1.21.4",
    ]
    ```

逗号等价于逻辑的 `AND` 算子：候选版本必须匹配所有给定版本子句，以便从整体上匹配说明符。

### Operators

| Operators | Function |
| :---: | --- |
| `~=` | [Compatible release](#compatible-release) |
| `==` | [Version matching](#version-matching) |
| `!=` | [Version exclusion](#version-exclusion) |
| `<=`, `>=` | [Inclusive ordered comparison](#ordered-comparison) |
| `<`, `>` | [Exclusive ordered comparison](#ordered-comparison) |
| `===` | [Arbitrary equality](#arbitrary-equality) |

### 版本匹配

版本匹配子句包括版本匹配算子 `==`  和版本标识符。

默认情况下，版本匹配算子基于严格的相等比较：指定的版本必须与请求的版本完全相同。

| Clause | Allowed versions |
| --- | --- |
| `==1` | `1.0.0` |
| `==1.2` | `1.2.0` |

通过在版本匹配子句的版本标识符后面附加一个后缀 `.*`，可以请求前缀匹配而不是严格的比较。这意味着在确定版本标识符是否匹配子句时，将忽略附加的尾随段。

| Clause | Allowed versions |
| --- | --- |
| `==1.*` | `>=1.0.0, <2.0.0` |
| `==1.2.*` | `>=1.2.0, <1.3.0` |

### 兼容发布

兼容发布子句由兼容发布算子 `~=` 和版本标识符组成。它匹配期望与指定版本兼容的任何候选版本。

对于给定的版本标识符 `V.N`，兼容版本子句大致等价于以下两个比较子句：

```
>= V.N, == V.*
```

此算子不能与单语义版本号一起使用，例如 `~=1`。

| Clause | Allowed versions |
| --- | --- |
| `~=1.2` | `>=1.2.0, <2.0.0` |
| `~=1.2.3` | `>=1.2.3, <1.3.0` |

### 版本排除

版本排除子句包含版本排除算子 `!=` 和版本标识符。

所允许的版本标识符和比较语义与 [版本匹配](#version-matching) 算子的版本标识符和比较语义相同，只是任何匹配的意义是相反的。

A version exclusion clause includes the version exclusion operator `!=` and a version identifier.

### 有序比较

包含性比较允许子句的版本标识符部分，而独占性比较则不允许。例如，`>=1.2` 允许版本为  `1.2.0`，而  `>1.2` 则不允许。

与包含式顺序比较 `<=` 和 `>=` 不同，排他式顺序比较 `<` 和 `>` 特别地排除了指定版本的预发布版本、发布后版本和本地版本。

### 任意相等

尽管非常不鼓励，但任意相等比较允许不带任何版本语义的简单字符串匹配，例如 `===foobar`。

## 环境标志

[环境标志](https://peps.python.org/pep-0508/#environment-markers) 允许只在满足某些条件时安装依赖项。

例如，如果你需要安装 `cryptography` 的最新版本，该版本可用于给定的 Python 主版本，你可以定义如下：

```
cryptography==3.3.2; python_version < "3"
cryptography>=35.0; python_version > "3"
```

或者，如果你只需要在 Python 3 上运行它在 Windows 上，你可以这样做：

```
cryptography; python_version ~= "3.0" and platform_system == "Windows"
```

可用的环境标记如下。

| Marker | Python equivalent | Examples |
| --- | --- | --- |
| `os_name` | `#!python import os`<br>`os.name` | <ul><li>posix</li><li>java</li></ul> |
| `sys_platform` | `#!python import sys`<br>`sys.platform` | <ul><li>linux</li><li>win32</li><li>darwin</li></ul> |
| `platform_machine` | `#!python import platform`<br>`platform.machine()` | <ul><li>x86_64</li></ul> |
| `platform_python_implementation` | `#!python import platform`<br>`platform.python_implementation()` | <ul><li>CPython</li><li>Jython</li></ul> |
| `platform_release` | `#!python import platform`<br>`platform.release()` | <ul><li>1.8.0_51</li><li>3.14.1-x86_64-linode39</li></ul> |
| `platform_system` | `#!python import platform`<br>`platform.system()` | <ul><li>Linux</li><li>Windows</li><li>Darwin</li></ul> |
| `platform_version` | `#!python import platform`<br>`platform.version()` | <ul><li>10.0.19041</li><li>\#1 SMP Fri Apr 2 22:23:49 UTC 2021</li></ul> |
| `python_version` | `#!python import platform`<br>`'.'.join(platform.python_version_tuple()[:2])` | <ul><li>2.7</li><li>3.10</li></ul> |
| `python_full_version` | `#!python import platform`<br>`platform.python_version()` | <ul><li>2.7.18</li><li>3.11.0b1</li></ul> |
| `implementation_name` | `#!python import sys`<br>`sys.implementation.name` | <ul><li>cpython</li></ul> |
| `implementation_version` | See [here](https://peps.python.org/pep-0508/#environment-markers) | <ul><li>2.7.18</li><li>3.11.0b1</li></ul> |

## 特性

可以使用[附加](https://peps.python.org/pep-0508/#extras)语法选择要安装的[可选依赖项](dependency.md#optional-dependencies)。例如，如果名为 `foo` 的依赖定义如下：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project.optional-dependencies]
    crypto = [
      "PyJWT",
      "cryptography",
    ]
    fastjson = [
      "orjson",
    ]
    cli = [
      "prompt-toolkit",
      "colorama; platform_system == 'Windows'",
    ]
    ```

你可以像这样选择  `cli` 和 `crypto` 特性：

```
foo[cli,crypto]==1.*
```

注意，特性紧接在包名之后，在任何 [版本说明符](#version-specifiers) 之前。

## 直接引用

与使用普通的[版本说明符](#version-specifiers)和从 PyPI 这样的索引获取包不同，您可以使用显式 [URI](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#Syntax) [直接引用](https://peps.python.org/pep-0440/#direct-references)  定义确切的源。

直接引用通常不用于已发布项目的依赖项，而是用于定义[环境的依赖项](environment/overview.md#dependencies)。

所有直接引用类型都以包名作为前缀：

```
<NAME> @ <REFERENCE>
```

### 版本控制系统

Various version control systems (VCS) are [supported](#supported-vcs) as long as the associated executable is available along your `PATH`.

VCS direct references are defined using one of the following formats:

```
<NAME> @ <SCHEME>://<PATH>
<NAME> @ <SCHEME>://<PATH>@<REVISION>
```

You may also append a `#subdirectory=<PATH>` component for specifying the relative path to the Python package when it is not located at the root e.g. `#subdirectory=lib/foo`.

For more information, refer to [this](https://pip.pypa.io/en/stable/topics/vcs-support/).

#### Supported VCS

=== "Git"
    | Executable | Schemes | Revisions | Example |
    | --- | --- | --- | --- |
    | `git` | <ul><li><code>git+file</code></li><li><code>git+https</code></li><li><code>git+ssh</code></li><li><code>git+http</code> :warning:</li><li><code>git+git</code> :warning:</li><li><code>git</code> :warning:</li></ul> | <ul><li>Commit hash</li><li>Tag name</li><li>Branch name</li></ul> | `proj @ git+https://github.com/org/proj.git@v1` |

=== "Mercurial"
    | Executable | Schemes | Revisions | Example |
    | --- | --- | --- | --- |
    | `hg` | <ul><li><code>hg+file</code></li><li><code>hg+https</code></li><li><code>hg+ssh</code></li><li><code>hg+http</code> :warning:</li><li><code>hg+static-http</code> :warning:</li></ul> | <ul><li>Revision hash</li><li>Revision number</li><li>Tag name</li><li>Branch name</li></ul> | `proj @ hg+file:///path/to/proj@v1` |

=== "Subversion"
    | Executable | Schemes | Revisions | Example |
    | --- | --- | --- | --- |
    | `svn` | <ul><li><code>svn+https</code></li><li><code>svn+ssh</code></li><li><code>svn+http</code> :warning:</li><li><code>svn+svn</code> :warning:</li><li><code>svn</code> :warning:</li></ul> | <ul><li>Revision number</li></ul> | `proj @ svn+file:///path/to/proj` |

=== "Bazaar"
    | Executable | Schemes | Revisions | Example |
    | --- | --- | --- | --- |
    | `bzr` | <ul><li><code>bzr+https</code></li><li><code>bzr+ssh</code></li><li><code>bzr+sftp</code></li><li><code>bzr+lp</code></li><li><code>bzr+http</code> :warning:</li><li><code>bzr+ftp</code> :warning:</li></ul> | <ul><li>Revision number</li><li>Tag name</li></ul> | `proj @ bzr+lp:proj@v1` |

### Local

You can install local packages with the `file` scheme in the following format:

```
<NAME> @ file://<HOST>/<PATH>
```

The `<HOST>` is only used on Windows systems, where it can refer to a network share. If omitted it is assumed to be `localhost` and the third slash must still be present.

The `<PATH>` can refer to a source archive, a wheel, or a directory containing a Python package.

| Type | Unix | Windows |
| --- | --- | --- |
| Source archive | `proj @ file:///path/to/pkg.tar.gz` | `proj @ file:///c:/path/to/pkg.tar.gz` |
| Wheel | `proj @ file:///path/to/pkg.whl` | `proj @ file:///c:/path/to/pkg.whl` |
| Directory | `proj @ file:///path/to/pkg` | `proj @ file:///c:/path/to/pkg` |

!!! tip
    You may also specify paths relative to your project's root directory on all platforms by using [context formatting](context.md#paths):

    ```
    <NAME> @ {root:uri}/pkg_inside_project
    <NAME> @ {root:uri}/../pkg_alongside_project
    ```

### Remote

You can install source archives and wheels by simply referring to a URL:

```
black @ https://github.com/psf/black/archive/refs/tags/21.10b0.zip
pytorch @ https://download.pytorch.org/whl/cu102/torch-1.10.0%2Bcu102-cp39-cp39-linux_x86_64.whl
```

An expected hash value may be specified by appending a `#<HASH_ALGORITHM>=<EXPECTED_HASH>` component:

```
requests @ https://github.com/psf/requests/archive/refs/tags/v2.26.0.zip#sha256=eb729a757f01c10546ebd179ae2aec852dd0d7f8ada2328ccf4558909d859985
```

If the hash differs from the expected hash, the installation will fail.

It is recommended that only hashes which are unconditionally provided by the latest version of the standard library's [hashlib module](https://docs.python.org/dev/library/hashlib.html) be used for hashes. As of Python 3.10, that list consists of:

- `md5`
- `sha1`
- `sha224`
- `sha256`
- `sha384`
- `sha512`
- `blake2b`
- `blake2s`

### Complex syntax

The following is an example that uses [features](#features) and [environment markers](#environment-markers):

```
pkg[feature1,feature2] @ <REFERENCE> ; python_version < "3.7"
```

Note that the space before the semicolon is required.
