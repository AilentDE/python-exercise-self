import { useState } from "react";

import SectiopnCard from "./SectionCard";
import liff from "@line/liff";

type UserInfo = {
  userId: string;
  displayName: string;
  pictureUrl?: string;
  accessToken: string | null;
};

const LineLiffSection = () => {
  const [liffInit, setLiffInit] = useState(false);
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);

  const fetchUserInfo = async () => {
    if (!liff.isLoggedIn()) return;

    const userProfile = await liff.getProfile();
    const accessToken = liff.getAccessToken();

    setUserInfo({
      userId: userProfile.userId,
      displayName: userProfile.displayName,
      pictureUrl: userProfile.pictureUrl,
      accessToken,
    });
  };

  if (!liffInit) {
    liff
      .init({ liffId: import.meta.env.VITE_LIFF_ID as string })
      .then(() => {
        setLiffInit(true);
        fetchUserInfo();
      })
      .catch((err) => {
        console.error(err);
      });
  }

  if (!liffInit)
    return <SectiopnCard title="Line LIFF">Loading...</SectiopnCard>;
  return (
    <SectiopnCard title="Line LIFF">
      {userInfo ? (
        <ul>
          <li>
            userId:
            <br />
            {userInfo.userId}
          </li>
          <li>
            displayName:
            <br />
            {userInfo.displayName}
          </li>
          <li>
            pictureUrl:
            <br />
            {userInfo.pictureUrl}
          </li>
          <li>
            accessToken:
            <br />
            {userInfo.accessToken}
          </li>
        </ul>
      ) : (
        "No-login"
      )}
    </SectiopnCard>
  );
};

export default LineLiffSection;
