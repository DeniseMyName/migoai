import requests

def get_token():
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://studio.flowgpt.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://studio.flowgpt.com/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    params = {
        'client': 'browser',
    }

    response = requests.get(
        'https://1816e4d6cd83.ba5a2ce6.us-east-2.token.awswaf.com/1816e4d6cd83/d1d994412487/inputs',
        params=params,
        headers=headers,
    )

    data = response.json()

    challenge = data.get("challenge", {})

    input_data = challenge.get("input")
    hmac = challenge.get("hmac")
    region = challenge.get("region")

    data = f'''{{
        "challenge": {{
            "input": "{input_data}",
            "hmac": "{hmac}",
            "region": "{region}"
        }},
        "solution": "0",
        "signals": [
            {{
                "name": "KramerAndRio",
                "value": {{
                    "Present": "OgAUawoj6Yim2cd8::8dfb5073f9c280a3b80dedf4d082f710::e648d37140618cfcb03ee9a006e9102080c0eac39f7c2da1f342c3d85626ea4244aa8fe9011f8ec3be8db7e62e481634deac1dd85da33dea0e59b2cc933e7d1ba21a85df33c9c881e34b282a9c65f787965059a6b7204d51549e87b8d7b3c4e136f4db332fc3bb5524d3947fdd28b0477e721a8ab7eb384b132424efef56b19e49882deb4f4c169ecf1697c14f31e702fe36858682a016baf5cd466d82d1c9d7933b59079de1af81ed60966082c2a641f0b7f8b426fa4aebdb0fbd98e643e9000a8b5b5aafcb9438c5c5a8bbda2569de4463f74e59fb586fc1fe9c3c21c4f48cd5cdab2a29f410c7eeee7ebf3b5eacbeea43f856c8e4b99fe2e0c12f1e0df7b7f69cdeb128a31fa1a5e11b18c800cae8c2577d49d78bea3325bcabfe2b921bd582d15fecfc3f203069d4087c328abdc2c837fa5049a0414f89c0e6643873a6a61151d1093a1582575f9f5adc6b4305d8e87df6137ba85d2fef3ba4167a02cadb09dce0697ad17f43a21539927019aff692c10f5e1dcb32be3cea692fe6494cae17b310304f768eb8462ecff778ecf941c07dd7396d7150f5b132d4b32785e562d790c2828c32acdafc0570eb770e118635b72e395b56e8dc2ff2df5cfe4427e8b93b0368a19342d30123bf0e423cec8f42258ee1e7750b3b52aa0231448d5ca27113d0141c2a21990b0eb0f9c089a371542738403b009e6a8f7599585030892217629e018b54b863b442d3aab2b2dfb052c4e4c56791659701336f97e38e818c05335c556ae8aeaea24d5c50e55cd0af5393729755636649e20bf15bbc5b56a99956dba2946f99e7e1e07afe490a9a9c03a61da67f4d33d19690f55748ebb2c594b79e515ee4cafd96e6872efa6d00abb29b412844f278d535a9729871b50493e2e999f495242b9dfd3ce4a1041686dd95b2ea27bf566b11689d12ceb9abef0fad694d32a52ca9b0b28c192b9ef6fa67eceb0ecedddfbe83b26d8475cb1cefe3f43d9a0a8fd72d04414e12808f48ee2888ad2faad45828e78118950803f9ad359596a80a987e9f29790aa46ef0d4ad10688f8bbccb06e120a8923c3fe1af9293214935d187ace11f28fa2263659216a3f0a96a1e21b6cffd28c952d1f29d9926c9963acff7ecc3029ad7a5482ef17831b7f9e6b2fbfcc518b2fd5c01bad67a2ee996815e0a5a38ea7cac31dc764928c36e29ae434788eaaffd1f67150a2d17ad30eb363623cf9e8cf617cc12de0aa68f4055f976dc54155634740fac1975d5c15380db476aa97f5dfc688c13882549c51e1741f0594413e185e53635c60492af6007187cf84fa169b445b0de7b2e209bacf0aaf0b42114995aabaa8a859e8bb0100d3c022b36a8bd879e7a6f8ef41ce19fa0206a46a4642a909d64c44c8a1098667af8ef51c1773b3540110b5fe4e9c3fdbc96bca8096f3f19ae1303cb75f78ab1b5e8b7f2ede1d4856dc124530ab5afb58d2265dc30e5ce70e423fa7bb28373526e11d0f1f9fe2a95e60691b5ea403914fb4b1c93438665849e25151e69337aaa466d1c3adf092c3b45f9442bd39252665a0ef5b52feb2cb14f16c72dc952c62689aae726e7fb69532a2bcbf1bab454bf33d3ba57c932be59c3ee280ef1f3da0a1b702ef55bf7f8bdfd5bf583dcb4c67a69536a305b919af523a9c88bb48634ef904549bcce9b6ef506bd440fd6c09a19f0cc1d59f659180e815c20acb9be74f0e380e6c53c82f2c135231b8a2f497b7c985c6528fc4af0b18ef4d061e27f38b358a9890853ae73541e00e13c2c5b3d2864253781001a3cd1ce82cdd74712055b4d1d1dfc1fae617a305fda3e870ad25cc4e9ee8afe4fa8c91514f64ac13890ce78c0b8851af0fe45da703bdb434373053c712e04dda1f8e8dfab2689bd8508db1eeb43bea984ac77f1d79f6f17d43c5839c63381a18faca05dfb1fb5e96f609685ece7b714b2561c1a29cd803ec59b289449a036744dc88e1372f491a7fdce95b2e595d5c2b69334610d11d593586cff97138e21c792e709d81c0c1ccf5cf349cdb8810f7271a45eef0dd5726cda7d4e11e45e9ea8b765d8c803c7f0d632358b418cbf3bbf9769c79914fe4e4f46caf3b7d1ab1ecf0dbeca0c51bdb4e68d7f6dccdaf7c3707be83e1044d162d00d4a6075ad610a799b4f72dc8ef72dfc80d4976689e50d4f049cc77d7797fc58e9bd6e5fff2c3b0498c1c7f036aa981500e5ed9deee0cc34d79f54290a69fd6d1e8e342b8e53df9c7199c6e6d509496265ab4020f8811ff2c824c95759aefa270798a96f91323a281338b44994ef5c52841609e92f8a5d1ea2bbc9fe7948d9809ea690dd3894182a995e8c939d56124cbc65851657f68138a3a6d0fdc78abd54ea69e9164445aa1033e2caf441f4160202c183f5f6432c6898beac9f9b402323aad1a3cea93acc2937489be365b5109782f1ad45272cba179e5098531fedcac9339dbca45fc0cc9340a015418d66cfa40921b29fcc2fcb71e3bd85b2e7d48dbfacd63860d10ceac7310b3ecbd1bf92847986cc46119ce3ce789d486fd2cc96e804da8fbfcb0df025fcae1f9bb1dca7ccebc206d9a788d2041170c5b45cd2bd0d7c205fe30e60229ae61bb02b89453ba70c177f4642db4b1ce3c29820bd7d7d76ddb6ad281da71ce8fe0d2ef9b97c976c0fabfefc898cd79812cb04939d713a756bcdeb08eaeaf0ac328f1d97dd264ffebb75421fa81ba63b0804cbdebdd16eaaf8f957f2fb8e78a1e2cf6a52f7592dbb504d6366ec254a31b47ae17e58c703b91a4cb534412adf73d48922701d70e80139cbc9b9eca604b517b923d63f77f00f6a3cc935cf7fbaa2ab425c6fd060571f5fdb675a9905ddc79b48317deeefe8d1dc0d997bdaa6ba93425408e92603813c4197fdf83c3be6cb4d24673b4204eb92cc390de7d142755b725659aa14999c3b824837f4b0dbf187f02e4c8581f3243ba71e9a8968bcbc58fb2a02ad8f15e56cac1ce4ce64eba37d829fef8aef8080d958025904e672d9953a8ebb2fdaa20ae5c2bbff2ef1b35d27af2d0e0a97cd874bc63cc6abca9d5fd80971eb6b5f3d75fa890b1dd57786cd807280d510f735fb5bf69496ad2fa0f9e3b4250c9757fb7e66f1bbec4813c2ab106a28db1948076cd618c84efe417cbe63de5049ca93d1ad23e86b75d85546cc508898d91e3c03eab50a39377d43340d62580fbe40abeb83d692d2b56189482566665622fe1d9aff1c50155d791fb3252b7ec34bf20ee48312ede1c2088f2b41c93cc5e8081586396fce95eaa6d64d72d77c5c84bf1ea133afad2bfee8b475d99141571f61ad7d521de5608677df385005d79bbc7b295d0386cca92618424641ab3a1654bf503e4de78958f051e34a867c41d31eb95675378be4ace6adaa61ca7519810272dd013b43fbab5f4a2e3746aaae9275a68ce0005bb8010b5e137753469a8c7fc68abbcd76e992f3e90f1f2e0901f92c15eb93a25425eb32c5dc54d8766e0bd573667bb35fb5de2d353dd34fd57c746d11c070cffa8a65cf0cfb9aac1be774329ca28de98c003a72b39f0498c0245adac1aa7282ec8d40a35c0d3d90c312a6c675d0708c3becb907c53480d6e6e84ead4aeaca4c3b3bfab85ee61d55c2d997a797d3e668f6a97d871939c63472eded576f58ecba179a10b8a58c43703059ebe778d744cdf6bd2d7dffaac3b9629444536eb0492721131129c2fd542ff37806ac1b8326dd464c83f34a068db692045c276c1ec765ff8899c7faedfb4146fb7e808e7e122971a84485004b9b06bcad62d0027f351154f73ddc8f1025e7f4f2e417e993ffdc610dffe79753e0daddf3fe707c682114ae37ccb52069576341ae98c24b35986fe4b20160d0a05070e1001e54d04301c5e5704aad6cf1fff35b3139cb08f111befd04dd5edc3bb4cdf2e99bc969385e0b4569f45441996bbb7f18770d2e223bdee94e1bea8cd49ae02a62d45253bbf0a0c56ec8f6ace0123de9bcd2cddc69182a4018c5027018ba89002a92d13c9fdfdd43fa4d49849ad82dfc410669858c781547e52cd984cf3268ee518035bd592e4586c6d00b6cc45158865568446cd4bf2352ced88f13d4b764a8369d466c61152b5035195fc1fd455e1b4ced4c46e60c8165f2a65651b6a966a9eb43a346b98b7ce8a0cb6957b58c2e28d70c529bd46dd57ef52d99b5b263ff801a57f3d081c6e906e3b41be5071b7e4bb1b9d7ca4bf7e2ace427660a53718b89e65c6ffba1fda3e18be82a5604ee8134561e1956119054bb46c330034be506ffb20e9c7e5ba792f1127fcd8f1a89c12bd8c713ba7a87d1db15e017ebcadb054a36c7e9d691c4ad0795cbfdf6d3ba0006d591351876e40f59b77981004f64f456f4dc233150824d94764ceb14907af06c8582e906ac6dc49ace8b0ef985464362697dd065328f86d54b3cabb270f6c2e1d79a72ce69f29b51a7fbe1da0c7b472843fb580efcd004a39a1a960cb49d1e8605f6c0f859125f9f1de7f8e988c58908957fec3a3b2e18dfafe2db1202c8cb469e73183b9858adc167dfbfa71bce18a6ff2ae277167f75719c22741cddf7aaeb0ce80705a2ee843e9a8fab7b9dbe0d053df465b1c36a04042213aa2417cbdb459805ca6860086ec1c3736560912d35fd5ebc6c95b45ff63c22b882ae0474617fb159daf73ef5da4e81f219339f0dda09819a407de1160cd8862941ffc548a54fc4ac0bffb825d754840914f2e5f84c99bd16d2470be1fea9f99c2a4222f1f2dc8cfad7a21badf41fb3b3e71070050fa8dedf5cae910b6daba169e6ecb96b87cb0d50d58d59e6fcfaaadb0e6f7baa2f48e61698aa284d3cad51de8ee20b2b75fe46a3e15e976abc51f90461c82a313013c2f3cfd746adf292b74f49cfd3efe4b7c7f4a749ed8c2e84859d7b86e91a281872c7f91895761bba7a3e404a0931301e1c1cccbcd0973fbbe73b6faa8037f4bcb0fc307e3ac2be081bda1150d5031de5e6b84d681abc467c7623b84c2d58f55e80d78f1a6988f68c315eda2aa0368a309dfe76774c327d3c4a2c90ac6db46f3d69658509160c5454f13d1514031d02e463a17f4f875d8ed747851ae6863bbc56f7deb13fbe4b3f27fe6da0ce8284edf0e868d6d762b68b9887eb1500e826951de629313ffe8fc0526503f4b5e92ab946609e147f0518e28c8b21f269449c37c98a90f47d3ec0f71e2a48d558fe4f48af"
                }}
            }}
        ],
        "checksum": "B72982EC",
        "existing_token": null,
        "client": "Browser",
        "domain": "studio.flowgpt.com",
        "metrics": [
            {{"name": "2", "value": 1.2000000029802322, "unit": "2"}},
            {{"name": "100", "value": 3, "unit": "2"}},
            {{"name": "101", "value": 3, "unit": "2"}},
            {{"name": "102", "value": 2, "unit": "2"}},
            {{"name": "103", "value": 57, "unit": "2"}},
            {{"name": "104", "value": 1, "unit": "2"}},
            {{"name": "105", "value": 0, "unit": "2"}},
            {{"name": "106", "value": 1, "unit": "2"}},
            {{"name": "107", "value": 0, "unit": "2"}},
            {{"name": "108", "value": 1, "unit": "2"}},
            {{"name": "undefined", "value": 1, "unit": "2"}},
            {{"name": "110", "value": 1, "unit": "2"}},
            {{"name": "111", "value": 47, "unit": "2"}},
            {{"name": "112", "value": 1, "unit": "2"}},
            {{"name": "undefined", "value": 3, "unit": "2"}},
            {{"name": "3", "value": 16.900000005960464, "unit": "2"}},
            {{"name": "7", "value": 0, "unit": "4"}},
            {{"name": "1", "value": 152.6000000089407, "unit": "2"}},
            {{"name": "4", "value": 32.8999999910593, "unit": "2"}},
            {{"name": "5", "value": 0.7000000029802322, "unit": "2"}},
            {{"name": "6", "value": 186.20000000298023, "unit": "2"}},
            {{"name": "0", "value": 882.2000000029802, "unit": "2"}},
            {{"name": "8", "value": 1, "unit": "4"}}
        ]
    }}'''


    response = requests.post(
        'https://1816e4d6cd83.ba5a2ce6.us-east-2.token.awswaf.com/1816e4d6cd83/d1d994412487/verify',
        headers=headers,
        data=data,
    )

    data = response.json()

    token = data.get("token")

    return token