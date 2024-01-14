Generic single-database configuration.

## ディレクトリ
migrationに関係するもの
```
src
├── alembic.ini
└── database ── migrations
                ├── README
                ├── env.py
                ├── script.py.mako
                └── versions
```
| ファイル名 | 説明 |
|--|--|
|alembic.ini| alembicのスクリプトが実行される時に読まれる構成ファイル。<br>実行時の設定を記述する。<br> - env.py の場所<br>- log の出力<br>- migration ファイルの命名規則 |
|env.py|マイグレーションツールが実行された時に必ず実行されるPythonスクリプト。<br>SQLAlchemyのEngineを設定や生成を行って、migrationが実行できるようにカスタマイズする。|
|script.py.mako|新しいmigrationのスクリプトを生成するために使用される Mako テンプレートファイル。<br>ここにあるものは何でもversions内の新しいファイルを生成するために使用される。|
|versions/|migrationスクリプトが保存されるディレクトリ|

## コマンド

カッコ内は省略可, [参考リンク](https://zenn.dev/shimakaze_soft/articles/4c0784d9a87751 )
### migrationファイルの自動生成
```
alembic revision --autogenerate -m "ファイル名"
./run.sh al(embic) c(reate)m(igration) "ファイル名"
```
### マイグレーションファイルの反映
```
alembic upgrade head
./run.sh al(embic) mi(grate)
```
### 履歴を見る
```
alembic history
./run.sh al(embic) history
```
### 更新の巻き戻し
戻したいmigrationFileのrevisionを指定
```
alembic downgrade 'revision'
./run.sh al(embic) downgrade 'revision'
```


https://alembic.sqlalchemy.org/en/latest/autogenerate.html
## Autogenerate は何を検出しますか (そして何を検出しませんか?)
Alembic に関するユーザーの問題の大部分は、自動生成によって確実に検出できる変更と検出できない変更の種類、および検出した変更に対して Python コードをどのようにレンダリングするかというトピックに集中しています。autogenerate は完璧を意図したものではないことに注意することが重要です。自動生成によって生成される移行候補を 手動で確認して修正することが常に必要です 。この機能はリリースが進むにつれてより包括的になり、エラーがなくなりつつありますが、現在の制限事項に注意する必要があります。

### 自動生成は以下を検出します:

- テーブルの追加、削除。
- 列の追加、削除。
- 列の NULL 可能ステータスの変更。
- インデックスと明示的に指定された一意制約の基本的な変更
- 外部キー制約の基本的な変更

### Autogenerate はオプションで以下を検出できます。

- 列タイプの変更。EnvironmentContext.configure.compare_typeこれは、パラメータを に 設定した場合に発生しますTrue。Numericデフォルトの実装は、と の間のような大きな変更を確実に検出しString、 などの SQLAlchemy の「ジェネリック」型によって生成された型にも対応します Boolean。長さや精度の値など、両方の型で共有される引数も比較されます。メタデータ タイプまたはデータベース タイプのいずれかに、もう一方のタイプの引数を超える追加の引数がある場合、これらは比較されません。たとえば、一方の数値タイプに「スケール」があり、もう一方のタイプにはそれがない場合、これはバッキング データベースがサポートしていないと見なされます。値、またはメタデータで指定されていないデフォルトについてレポートします。
- 型比較ロジックも完全に拡張可能です。詳細については、タイプの比較を参照してください 。
- サーバーのデフォルトの変更。EnvironmentContext.configure.compare_server_default これは、パラメータをTrue、またはカスタム呼び出し可能関数に設定した場合に発生します。この機能は単純な場合にはうまく機能しますが、常に正確な結果が得られるとは限りません。Postgresql バックエンドは、実際にデータベースに対して「検出された」値と「メタデータ」値を呼び出して、同等性を判断します。この機能はデフォルトではオフになっているため、最初にターゲット スキーマでテストできます。型比較と同様に、呼び出し可能オブジェクトを渡すことでカスタマイズすることもできます。詳細については、関数のドキュメントを参照してください。

### 自動生成では次のものを検出できません:
- テーブル名の変更。これらは 2 つの異なるテーブルの追加/削除として表示されるため、代わりに手動で編集して名前を変更する必要があります。
- 列名の変更。テーブル名の変更と同様、これらは列の追加/削除のペアとして検出されますが、名前の変更とはまったく同じではありません。
- 匿名の名前付き制約。制約に名前を付けます (例: ) 。制約の自動命名スキームを構成する方法の背景については、「命名制約の重要性」セクションを参照してください 。UniqueConstraint('col1', 'col2', name="my_name")
- EnumENUM を直接サポートしていないバックエンドで生成された場合などの特殊な SQLAlchemy 型。これは、サポートしていないデータベースでのそのような型の表現、つまり CHAR+ CHECK 制約が、あらゆる種類の CHAR+CHECK になる可能性があるためです。SQLAlchemy がこれが実際に ENUM であると判断するのは単なる推測であり、一般的には悪い考えです。ここで独自の「推測」関数を実装するには、 sqlalchemy.events.DDLEvents.column_reflect()イベントを使用して CHAR (またはターゲットの型) が反映されたことを検出し、それが目的であることがわかっている場合は、それを ENUM (または必要な型) に変更します。タイプの。これを sqlalchemy.events.DDLEvents.after_parent_attach() 自動生成プロセス内で使用して、不要な CHECK 制約をインターセプトしてアタッチを解除することができます。

### 現在のところ自動生成はできませんが、最終的には次のものを検出します。
- PRIMARY KEY、EXCLUDE、CHECK など、一部の独立した制約の追加と削除はサポートされない場合があります。これらは必ずしも自動生成検出システム内に実装されているわけではなく、サポートされている SQLAlchemy 方言でもサポートされていない可能性があります。
- シーケンスの追加、削除 - まだ実装されていません。