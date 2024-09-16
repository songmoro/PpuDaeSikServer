### Overview
데이터를 스크래핑하고 노션 API를 호출해 데이터베이스를 업데이트하는 레포입니다.

Github Actions의 Crontab으로 주기적으로 스크래핑, 업데이트 코드를 수행하며, 노션 Auth Key, 노션 DB ID와 같은 노출되지 않아야하는 요소는 Github Actions - Secrets을 통해 관리되어 열람할 수 없으니 참고 바랍니다.
Secrets은 코드 수행시 주입되어 사용됩니다.

### 스크래핑 코드 구동
![screenrecord-1](https://github.com/user-attachments/assets/e5cf820f-ec3d-4aec-8d24-78af193ed16e)
