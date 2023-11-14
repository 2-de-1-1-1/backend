# backend

## Local Run(on SQLLITE3)
<pre>
  <code>
    python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic
    python manage.py runserver 
  </code>
</pre> 


## Local Run(on AWS AZURE SQL)
### prerquisites
1. MS SQL ODBC 18 설치 (https://learn.microsoft.com/ko-kr/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16)
2. 환경변수 세팅(Notion 프로젝트 위키 > DB 접근 정보 및 가이드 참조)

<pre>
  <code>
    cd career_site
    python manage.py collectstatic
    python manage.py runserver --settings career_site.production
  </code>
</pre>
