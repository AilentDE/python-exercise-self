class RichmenuSample:
    login = (
        {
            "tab_a": {
                "size": {"width": 2500, "height": 1686},
                "selected": False,
                "name": "richmenu-login-tab-a",
                "chatBarText": "選單",
                "areas": [
                    {
                        "bounds": {"x": 800 + 50, "y": 0, "width": 800, "height": 200},
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-login-tab-b",
                            "data": "action=switch&from=richmenu-login-tab-a&to=richmenu-login-tab-b",
                        },
                    },
                    {
                        "bounds": {"x": 800 * 2 + 50 * 2, "y": 0, "width": 800, "height": 200},
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-login-tab-c",
                            "data": "action=switch&from=richmenu-login-tab-a&to=richmenu-login-tab-c",
                        },
                    },
                ],
            },
            "tab_b": {
                "size": {"width": 2500, "height": 1686},
                "selected": False,
                "name": "richmenu-login-tab-b",
                "chatBarText": "選單",
                "areas": [
                    {
                        "bounds": {"x": 0, "y": 0, "width": 800, "height": 200},
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-login-tab-a",
                            "data": "action=switch&from=richmenu-login-tab-b&to=richmenu-login-tab-a",
                        },
                    },
                    {
                        "bounds": {"x": 800 * 2 + 50 * 2, "y": 0, "width": 800, "height": 200},
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-login-tab-c",
                            "data": "action=switch&from=richmenu-login-tab-b&to=richmenu-login-tab-c",
                        },
                    },
                ],
            },
            "tab_c": {
                "size": {"width": 2500, "height": 1686},
                "selected": False,
                "name": "richmenu-login-tab-c",
                "chatBarText": "選單",
                "areas": [
                    {
                        "bounds": {"x": 0, "y": 200, "width": 2500, "height": 1486},
                        "action": {
                            "type": "uri",
                            "label": "liff",
                            "uri": "https://liff.line.me/2006790295-j2GxEnYX",
                        },
                    },
                    {
                        "bounds": {"x": 0, "y": 0, "width": 800, "height": 200},
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-login-tab-a",
                            "data": "action=switch&from=richmenu-login-tab-c&to=richmenu-login-tab-a",
                        },
                    },
                    {
                        "bounds": {"x": 800 + 50, "y": 0, "width": 800, "height": 200},
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-login-tab-b",
                            "data": "action=switch&from=richmenu-login-tab-c&to=richmenu-login-tab-b",
                        },
                    },
                ],
            },
        },
    )
    without_login = (
        {
            "tab_a": {
                "size": {"width": 2500, "height": 1686},
                "selected": False,
                "name": "richmenu-without-login-tab-a",
                "chatBarText": "選單",
                "areas": [
                    {
                        "bounds": {"x": 0, "y": 200, "width": 2500, "height": 1486},
                        "action": {
                            "type": "postback",
                            "label": "login",
                            "data": "action=login",
                            "displayText": "我要登入",
                            "inputOption": "closeRichMenu",
                        },
                    },
                    {
                        "bounds": {"x": 800 + 50, "y": 0, "width": 800, "height": 200},
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-without-login-tab-b",
                            "data": "action=switch&from=richmenu-without-login-tab-a"
                            "&to=richmenu-without-login-tab-b",
                        },
                    },
                    {
                        "bounds": {"x": 800 * 2 + 50 * 2, "y": 0, "width": 800, "height": 200},
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-without-login-tab-c",
                            "data": "action=switch&from=richmenu-without-login-tab-a"
                            "&to=richmenu-without-login-tab-c",
                        },
                    },
                ],
            },
            "tab_b": {
                "size": {"width": 2500, "height": 1686},
                "selected": False,
                "name": "richmenu-without-login-tab-b",
                "chatBarText": "選單",
                "areas": [
                    {
                        "bounds": {"x": 0, "y": 0, "width": 800, "height": 200},
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-without-login-tab-a",
                            "data": "action=switch"
                            "&from=richmenu-without-login-tab-b&to=richmenu-without-login-tab-a",
                        },
                    },
                    {
                        "bounds": {"x": 800 * 2 + 50 * 2, "y": 0, "width": 800, "height": 200},
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-without-login-tab-c",
                            "data": "action=switch&from=richmenu-without-login-tab-b"
                            "&to=richmenu-without-login-tab-c",
                        },
                    },
                ],
            },
            "tab_c": {
                "size": {"width": 2500, "height": 1686},
                "selected": False,
                "name": "richmenu-without-login-tab-c",
                "chatBarText": "選單",
                "areas": [
                    {
                        "bounds": {"x": 0, "y": 200, "width": 2500, "height": 1486},
                        "action": {
                            "type": "uri",
                            "label": "liff",
                            "uri": "https://liff.line.me/2006790295-j2GxEnYX",
                        },
                    },
                    {
                        "bounds": {"x": 0, "y": 0, "width": 800, "height": 200},
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-without-login-tab-a",
                            "data": "action=switch&from=richmenu-without-login-tab-c"
                            "&to=richmenu-without-login-tab-a",
                        },
                    },
                    {
                        "bounds": {"x": 800 + 50, "y": 0, "width": 800, "height": 200},
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-without-login-tab-b",
                            "data": "action=switch&from=richmenu-without-login-tab-c"
                            "&to=richmenu-without-login-tab-b",
                        },
                    },
                ],
            },
        },
    )
    asset_path = (
        {
            'login': {
                'tab_a': 'assets/login-A.png',
                'tab_b': 'assets/login-B.png',
                'tab_c': 'assets/login-C.png',
            },
            'without_login': {
                'tab_a': 'assets/without-login-A.png',
                'tab_b': 'assets/without-login-B.png',
                'tab_c': 'assets/without-login-C.png',
            },
        },
    )
