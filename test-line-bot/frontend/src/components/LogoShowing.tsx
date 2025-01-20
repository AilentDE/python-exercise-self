import reactLogo from "../assets/react.svg";
import lineLogo from "../assets/line.svg";

const LogoShowing = () => {
  return (
    <>
      <div>
        <a
          href="https://developers.line.biz/en/reference/messaging-api/"
          target="_blank"
        >
          <img src={lineLogo} className="logo line" alt="Line logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Line + React</h1>
    </>
  );
};

export default LogoShowing;
