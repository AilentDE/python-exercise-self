import { useEffect, useRef, useState } from "react";
import CryptoJS from "crypto-js";

import SectiopnCard from "./SectionCard";
import { exchangeUserToken, UserToken } from "../action/line";

type UserInfo = {
  userId: string;
  displayName: string;
  pictureUrl?: string;
};

const LineLoginSection = () => {
  const [userToken, setUserToken] = useState<UserToken | null>(null);
  const [user, setUser] = useState<UserInfo | null>(null);
  const requested = useRef(false);
  const params = new URLSearchParams(window.location.search);
  const state = params.get("state");
  const code = params.get("code");

  useEffect(() => {
    const fetchUserInfo = async () => {
      if (!code) return;
      if (requested.current) {
        return;
      } else {
        requested.current = true;
      }

      await exchangeUserToken(code, setUserToken);
    };

    fetchUserInfo();
  }, [code]);

  if (!state || !code)
    return <SectiopnCard title="Line Login">No-login</SectiopnCard>;

  if (userToken && !user) {
    const payload = userToken.id_token.split(".")[1];
    const decodedPayload = JSON.parse(atob(payload));
    const varified = CryptoJS.SHA1(decodedPayload.sub).toString() === state;
    if (!varified) {
      alert("Invalid user");
      return;
    } else {
      setUser({
        userId: decodedPayload.sub,
        displayName: decodedPayload.name,
        pictureUrl: decodedPayload.picture,
      });
    }
  }

  return (
    <SectiopnCard title="Line Login">
      <ul>
        <li>
          state:
          <br />
          {state}
        </li>
        <li>
          code:
          <br />
          {code}
        </li>
        {userToken ? (
          <>
            <li>
              access_token:
              <br />
              {userToken.access_token}
            </li>
            <li>
              refresh_token:
              <br />
              {userToken.refresh_token}
            </li>
            <li>
              id_token:
              <br />
              {userToken.id_token}
            </li>
          </>
        ) : (
          <li>loading...</li>
        )}
        {user && (
          <>
            <li>
              userId:
              <br />
              {user.userId}
            </li>
            <li>
              displayName:
              <br />
              {user.displayName}
            </li>
            {user.pictureUrl && (
              <li>
                pictureUrl:
                <br />
                <img src={user.pictureUrl} alt="profile" />
              </li>
            )}
          </>
        )}
      </ul>
    </SectiopnCard>
  );
};

export default LineLoginSection;
