import SectiopnCard from "./SectionCard";

const LineLoginSection = () => {
  const params = new URLSearchParams(window.location.search);
  const state = params.get("state");
  const code = params.get("code");

  return (
    <SectiopnCard title="Line Login">
      <ul>
        <li>
          state:
          <br />
          {state ? state : "undefined"}
        </li>
        <li>
          code:
          <br />
          {code ? code : "undefined"}
        </li>
      </ul>
    </SectiopnCard>
  );
};

export default LineLoginSection;
