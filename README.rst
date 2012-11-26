===========================
Command Line Tools for CODE
===========================

这是一个方便使用 `code`_ 进行合作开发的工具。

.. _code: http://code.dapps.douban.com

Install
=======

全局安装::

  sudo pip install -e git+http://code.dapps.douban.com/codecli.git#egg=codecli

或者安装在 $HOME/.local 下::

  pip install --user -e git+http://code.dapps.douban.com/codecli.git#egg=codecli
  # add $HOME/.local/bin to your $PATH

Usage
=====

从一个现有仓库 fork 一份（这部分目前只能手工操作，等code提供fork api后可自动进
行）:


创建本地clone
~~~~~~~~~~~~~~

::

    $ code fork {repo} {your_fork} {dir}
    $ cd dir

其中，repo 和 your_fork 只需要填写在 code 上的项目名即可，例如::

    $ code fork dae dae_hongqn dae

开始一个分支
~~~~~~~~~~~~

::

  code start {branch-name}

会自动从最新的master创建分支。

与master同步
~~~~~~~~~~~~

::

  code sync

提交pull request
~~~~~~~~~~~~~~~~

::

    code pullreq

会自动merge master然后打开浏览器直达创建pull request页面。
