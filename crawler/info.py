# 정보나루 API_KEY
API_KEY = "b16e988e037cc5343832a554bb1b66a8574ca50de3147198b039c425374b94ad"
library_info = {
    "requestUrl": f"http://data4library.kr/api/libSrch?authKey={API_KEY}&pageSize=100",
    "description": """
        libCode: 도서관 코드
        libName: 도서관 명
        address: 주소
        tel: 전화번호
        fax: FAX 번호
        latitude: 위도
        longitude: 경도
        homepage: 홈페이지 URL
        closed: 휴관일
        operationTime: 운영시간
        bookCount: 보유 단행본수
    """
}

# kakao REST API key
KAKAO_API_KEY = "8bdcd25c1ad212c6bf644fa3752ddbac"
kakao_book = {
    "requestUrl": "https://dapi.kakao.com/v3/search/book?target=publisher&query=",
    "headers" : {
        "Authorization": f"KakaoAK {KAKAO_API_KEY}"
    }
}