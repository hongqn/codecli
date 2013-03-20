===========================
Command Line Tools for CODE
===========================

.. image:: http://code.dapps.douban.com/codecli/raw/master/images/codecli-256.png

这是一个方便使用 `code`_ 进行合作开发的工具。

.. _code: http://code.dapps.douban.com

Install
=======

使用 virtualenv::

  $ virtualenv codecli
  $ codecli/bin/pip install -e git+http://code.dapps.douban.com/codecli.git#egg=codecli
  $ ln -s `pwd`/codecli/bin/code $HOME/bin/
  # make sure add $HOME/bin to your $PATH

Usage
=====

创建本地clone
~~~~~~~~~~~~~~

如果你要向一个仓库贡献代码，先在 code 上从其 fork 一份（这部分目前只能手工操作
，等code提供fork api后可自动进行），然后运行


::

    $ code fork {repo} {your_fork} {dir}
    $ cd dir

其中，repo 和 your_fork 只需要填写在 code 上的项目名即可，例如::

    $ code fork codecli hongqn/codecli codecli


如果你只是想管理自己的仓库，而不是向其他人的仓库贡献代码，可以用 ``code
clone`` 命令::

    $ code clone codecli


``code fork`` 和 ``code clone`` 命令都会创建 ``origin`` 和 ``upstream`` 两个
remote ，在 codecli 的其他命令中，会默认这两个 remote 均存在， ``origin`` 指向
你自己的fork， ``upstream`` 指向上游仓库（即你希望贡献代码的仓库）。对于使用
``code clone`` 的仓库而言， ``origin`` 和 ``upstream`` 均指向你自己的仓库。

同时， codecli 还会设置 user.email 和 user.name ，并保存在 ~/.codecli.conf 中
。之后每次使用 codecli 创建本地仓库时，都会自动从 ~/.codecli.conf 中读取之前保
存的用户信息。


开始一个分支
~~~~~~~~~~~~

任何时候，你想开发一个新的 feature 、修改一个 bug 、甚至只是修复一个 typo 时，
都可以使用如下命令::

    code start {branch-name}

会自动从最新的upstream/master创建分支。相当于::

    git fetch upstream
    git checkout -b {branch} --no-track upstream/master

不用担心创建了太多 branch 发送 pullreq 时选择麻烦， codecli 为你提供了快速提交
pullreq 的方法（见 `提交pull request`_ ）。

与upstream/master同步
~~~~~~~~~~~~~~~~~~~~~

当你的分支开发了一段时间，希望和上游其他人已经提交的改动合并，以便可以确保你的
改动在最新代码上也可正常工作时，你需要同步上游代码::

    code sync

相当于::

    git fetch upstream
    git merge upstream/master

可以用 ``--rebase`` 参数（缩写为 ``-r`` ）指定执行 ``git rebase`` 而非 ``git
merge`` 。

如果你的分支是从 ``code hotfix`` （见 `从非master分支进行hotfix`_ ） 创建的，
不用担心， codecli 会正确处理，不会不小心把 master merge 进来弄得一团糟。

提交pull request
~~~~~~~~~~~~~~~~

当你的新 feature 或者 bugfix 已经完成，准备提交 pullreq 时（当然建议你先用 ``git
rebase -i`` 清理一下提交，squash 无意义的 oops 或者 tmpsav 之类的 commits 先）
，在你的分支下执行如下命令::

    code pr

会自动 merge master ， push 到 origin ，然后打开浏览器直达创建 pull request 页
面。相当于::

    code sync
    git push --set-upstream origin {branch}
    open http://code.dapps.douban.com/{upstream}/newpull/new?head_ref={branch}&base_ref=master

如果是 hotfix 分支， 也会设置正确的目标分支 （比如 ``release`` ）

从非master分支进行hotfix
~~~~~~~~~~~~~~~~~~~~~~~~

不少对稳定性有要求的项目在线上部署的不是 master 分支，而是其他分支（常见的是
``release`` 分支）。如果发现一个线上 bug 需要立刻修复，但此时 master 已经有了
一些新的改动，如果在 master 上修复然后 merge 到 release 上的话，可能解决了此问
题但又带来了新的问题。所以希望只上线针对紧急bug的改动。

这时你需要 codecli 的 hotfix 功能::

    code hotfix {release-branch-name} {hotfix-name}

其中 {release-branch-name} 为线上 branch 名，例如::

    code hotfix release ahbei-404

会从 upstream/{release-branch-name} 创建分支，起名为hotfix-{release-branch-name}-{hotfix-name} 。相当于::

    git fetch upstream
    git checkout -b hotfix-release-ahbei-404 --no-track upstream/release

当执行 ``code pr`` 时，会自动将目标分支指向 {release-branch-name} 。


checkout 到某个 pullreq
~~~~~~~~~~~~~~~~~~~~~~~

在 review 某个 pullreq 时，有时我们希望能够在本地 checkout 改动的代码，以便在
本地执行单元测试、调试等工作。感谢 code 提供的 `使用refs拉取pr
<http://code.dapps.douban.com/code/docs/pages/pr-refs-and-grunt.html>`_ 的功能
，可以用如下命令::

    code pr {pr_id}

抓取指定 pullreq 并自动 checkout 到它的代码。 


fetch 其他人的 fork
~~~~~~~~~~~~~~~~~~~

当合作开发一个项目时，可能其他人也有对 upstream 项目的 fork，有时你需要
checkout 或者 merge 他的代码。手工用长长的 git url 加 remote 然后 fetch ？不用
那么麻烦，用 ``code fetch`` 轻松搞定::

    code fetch {username}

即可自动创建一个新的 remote ，指向其他人的 fork ，并 fetch 之。相当于::

    git remote add {username} http://code.dapps.douban.com/{username}/{repo}.git
    git fetch {username}

这要求其他人的 fork 遵循 code 的新的二级目录的结构（即 username/repo）。如果
origin 也是一个 fork 的话，也需要遵循此结构。

end 分支的开发
~~~~~~~~~~~~~~~~~~~

当结束一个功能的开发时, 你可以用 ``code end`` 来搞定::

    code sync
    code end {branchname}

即可自动删除远程和本地的branch, 结束这个功能的开发。相当于::

    git br -d {branchname}
    git push origin :{branchname}


让code与git命令结合更紧密
~~~~~~~~~~~~~~~~~~~~~~~~~

在使用codecli的时候，经常会出现一会使用code命令一会使用git命令的情况，为了让两个命令结合更紧密，你可以配置一下~/.gitconfig，参考配置如下::

    [alias]
    start = !code start
    pr = !code pr
    sync = !code sync
    end = !code end
