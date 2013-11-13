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

``your_fork``和``dir``可以忽略，默认值分别为``{user_name}/{repo}``和``{repo}``，例如::

    $ code fork codecli

就等同于前一个例子(需要确保你在~/.codecli.conf里设置了user.email)


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

加 ``-t`` 参数可以给其他人的 fork 提交 pull request，比如::

    code pr -t satoru

此时，也可以用 ``user:branch`` 的形式，指定向其他人的指定 branch 提交 pull
request，比如::

    code pr -t satoru:zsh_completion


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

用 ``-t`` 参数可以 checkout 到某个用户的 fork 上的 pull request 。

在 checkout 到 pullreq 后，如果此 pullreq 还有后续提交，可以使用::

  code sync

命令进行同步。并且还可以在本地编辑代码，提交。然后使用::

  code pr

命令向此 pullreq 的发起仓库的对应分支发起 pullreq 。当发起人 merge 了你的
pullreq 后，你提交的改动会自动出现在最初的 pullreq 中。


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

branchname 缺省值为当前 branch ，所以用 ``code end`` 会直接删除当前的 branch。

如果需要同时删除多个 branch ，也可以用 ``code end br1 br2 br3`` 这种方式。


将 upstream 的一个分支 merge 到另一个分支
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如果你维护的项目采用如 release 这样的分支标记正式上线版本和开发版本，并且用
``code hotfix`` 命令来给线上版本做 hotfix ，那么你可能会经常有这样两个需求：

1. 把 master 分支中的 commits 合并到 release 分支，准备上线。
2. 把做了 hotfix 的 release 分支中的改动合并到 master 分支中。

这时，你可以用 ``code merge`` 命令来简化操作。对第一种情况，执行::

    code merge master release

会发起一个将 upstream 中的 master 分支合并到 release 分支的 pull request。对
第二种情况，执行::

    code merge release master

则会发起一个从 release 到 master 的 pull request 。

使用 ``--push`` 参数可以在本地创建一个分支执行 merge 操作，然后直接 push 到
upstream （需要有 upstream 的 push 权限）。如果有冲突，可以在本地修复冲突后，
重新用 ``--push`` 运行。


定制 webbrowser 的行为
~~~~~~~~~~~~~~~~~~~~~~

在发送 pullreq 时，codecli 会使用默认浏览器打开 code 的提交界面。可以用以下命
令来定制此行为：

    code config webbrowser.name firefox

指定使用 Firefox 来打开。此处可选择的值为 Python 的 webbrowser_ 模块中注册的名字。

.. _webbrowser: http://docs.python.org/2.7/library/webbrowser.html

    code config webbrowser.name /path/to/executable

使用指定脚本打开，待打开的 URL 会作为参数传递给脚本。

    code config webbrowser.name none

不使用浏览器打开，仅在终端显示URL地址。

    code config webbrowser.name --unset

恢复成使用默认浏览器打开。


让code与git命令结合更紧密
~~~~~~~~~~~~~~~~~~~~~~~~~

在使用codecli的时候，经常会出现一会使用code命令一会使用git命令的情况，为了让两个命令结合更紧密，你可以配置一下~/.gitconfig，参考配置如下::

    [alias]
    start = !code start
    pr = !code pr
    sync = !code sync
    end = !code end

zsh下的code命令补全
~~~~~~~~~~~~~~~~~~~

将 ``_code`` 复制到 ``$fpath`` 中的某个目录，重启 zsh 就可以。


ChangeLog
=========

2013-11-13

* bugfix: 修复当 ``webbrowser.name`` 未设置或者设置为 script 时会抛异常的问题。
  Thank xupeng!

2013-11-08
~~~~~~~~~~

* feature: 增加 ``code config`` 命令，可以使用 ``code config webbrowser.name``
  定制 webbrowser 行为。
* feature: 允许 ``code clone`` 使用URL作为参数。 Thank satoru!
* feature: ``code fork`` 时默认使用自己的fork仓库名。 Thank satoru!
* feature: ``code fork`` 时默认 clone 到仓库同名目录。 Thank satoru!
* feature: 支持 code ssh url。 Thank chenzheng and yaofeng!
* feature: 允许 ``code end`` 结束多个 branches。  Thank satoru!
* bugfix: 修正当仓库名中含有 ``g`` ``i`` ``t`` 字符时会出错的问题。 Thank anrs!
* bugfix: 修复判断分支是否已经 push 到 remote 的方法，避免误判。  Thank satoru!
* bugfix: 修复重复开启 pr-on-pr 会出错的问题。  Thank menghan!

2013-07-11
~~~~~~~~~~

* 在首次发 pullreq 的 branch 上使用 rebase master 代替 merge master，减少无谓
  的 merge commit

2013-07-11
~~~~~~~~~~

* docfix: 修正了 ``code fork --help`` 帮助信息中的样例仓库名 (thank satoru)

* bugfix: ``code merge --push`` 没有执行 ``git fetch upstream`` ，导致 merge
  的数据不是最新的

2013-06-26
~~~~~~~~~~

* ``code end`` 命令增加 ``-f`` 参数，可删除未 push 的分支 (thank guibog)

2013-06-18
~~~~~~~~~~

* 允许 remote 为 "用户名@" 的形式的 URL (thank guibog)

2013-06-13
~~~~~~~~~~

* bugfix: 在非 git repo 目录下运行 code 会出错

2013-06-09
~~~~~~~~~~

* ``code end`` 命令默认关闭当前分支 (thank guibog)

2013-06-04
~~~~~~~~~~

* 增加 ``code merge`` 命令，简化 release 分支的管理。

2013-05-20
~~~~~~~~~~

* ``code pr -t`` 参数支持指定目标仓库的 branch。

2013-04-01
~~~~~~~~~~

* ``code start`` 时如果目标 branch 已存在，会提示是要切换还是重建。

2013-03-26
~~~~~~~~~~

* 不使用 ``commands.getoutput`` ，以支持windows
