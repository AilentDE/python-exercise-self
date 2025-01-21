const BASE_URL = import.meta.env.VITE_BACKEND_URL;

export type UserToken = {
  access_token: string;
  refresh_token: string;
  id_token: string;
};

export const exchangeUserToken = async (
  code: string,
  callback: (tokenSet: UserToken) => void
): Promise<string | undefined> => {
  const url = BASE_URL + "/line/login";
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        code,
      }),
    });
    if (!response.ok) {
      console.error(response.statusText);
      return;
    }
    const data: UserToken = await response.json();
    callback(data);
  } catch (error) {
    alert("error: " + error);
    console.error(error);
  }
};
