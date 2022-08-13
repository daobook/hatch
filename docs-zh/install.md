# 安装

-----

## pip

Hatch 可在 PyPI 上使用，并且可以通过 [pip](https://pip.pypa.io) 安装。

```
pip install hatch
```

!!! warning
    此方法修改您选择安装的 Python 环境。

## pipx

[pipx](https://github.com/pypa/pipx) 允许在隔离的环境中全局安装 Python 应用程序。

```
pipx install hatch
```

## Homebrew

阅读 [formula](https://formulae.brew.sh/formula/hatch) 了解更多细节。

```
brew install hatch
```

## Conda

阅读 [feedstock](https://github.com/conda-forge/hatch-feedstock) 了解更多细节。

```
conda install -c conda-forge hatch
```

或者使用 [mamba](https://github.com/mamba-org/mamba)：

```
mamba install hatch
```

## MacPorts

阅读 [port](https://ports.macports.org/port/hatch/) 了解更多细节。

```
sudo port install hatch
```

## Fedora

The minimum supported version is 37, currently in development as [Rawhide](https://docs.fedoraproject.org/en-US/releases/rawhide/).

```
sudo dnf install hatch
```

## Void Linux

```
xbps-install hatch
```

## 构建系统的可用性

Hatchling is Hatch's [build backend](config/build.md#build-system) which you will never need to install manually. See its [changelog](history.md#hatchling) for version information.

[![Packaging status](https://repology.org/badge/vertical-allrepos/hatchling.svg){ loading=lazy }](https://repology.org/project/hatchling/versions)
