## https://test-notepad-deploy.fly.dev/api/question/list

## 게시판

배포: fly.io
프레임워크: Fastapi, jinja2
데이터베이스: postgres

![image](https://github.com/KANGSEONGGU4/Noticeboard/assets/132239219/70fa3a36-bbf0-47b9-ba24-141f887e998a)


Fastapi와 jinja2를 이용하여 게시판을 만들게 되었습니다.

웹 프레임워크를 사용하기 이전에 fastapi로만 웹페이지를 만들면 어떠한 불편함이 있을까에 대한 궁금증이 생겨서 fastapi와 jinja2만 사용하여 이 프로젝트를 만들게 됐습니다.

## 추가 사항
- 회원가입 완료시 바로 자동 토큰을 발행해 로그인이 가능하도록 구현
- 댓글을 작성시 작성자가 표시되며 수정, 삭제 버튼 추가


## 오류 사항

```
Traceback (most recent call last):
  File "/Users/kangseonggu/Study/test_notepad/test.py", line 44, in <module>
    access_token = create_access_token(data={"username": "john_doe"}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
  File "/Users/kangseonggu/Study/test_notepad/test.py", line 23, in create_access_token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
AttributeError: module 'jwt' has no attribute 'encode'
```

```
-> 기존에 있던 jwt를 삭제후 pyjwt를 설치하여 오류 해결
```

```
(trapped) error reading bcrypt version
Traceback (most recent call last):
  File "/usr/local/Caskroom/miniconda/base/envs/test/lib/python3.10/site-packages/passlib/handlers/bcrypt.py", line 620, in _load_backend_mixin
    version = _bcrypt.__about__.__version__
AttributeError: module 'bcrypt' has no attribute '__about__'
```
```
-> 공식문서 및 유저 커뮤니티를 확인한 결과 bcypy 4.1.2 버전은 오류가 발생하여 4.0.1 버전으로 설치하여 오류 해결
```

```
document.getElementById("password1").addEventListener("input", function() {
            var password1 = document.getElementById("password1").value;
            var maskedPassword1 = "*".repeat(password1.length);
            document.getElementById("password1").setAttribute("value", password1);
            document.getElementById("password1").value = maskedPassword1;
        });
        
        document.getElementById("password2").addEventListener("input", function() {
            var password2 = document.getElementById("password2").value;
            var maskedPassword2 = "*".repeat(password2.length);
            document.getElementById("password2").setAttribute("value", password2);
            document.getElementById("password2").value = maskedPassword2;
        });
```

```
-> 패스워드 입력시 *로 로그인 시 패스워드가 노출되지 않게 코드를 작성해 보았지만 화면에서만 *로 표시가 되는 것이 아닌 실제 비밀번호가 *로 변경되기 때문에 오류 발생하여 해결 완료하였다
```

