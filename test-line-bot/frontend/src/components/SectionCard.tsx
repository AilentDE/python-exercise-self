type SectiopnCardProps = {
  title?: string;
  children: React.ReactNode;
};

const SectiopnCard = ({ title, children }: SectiopnCardProps) => {
  return (
    <div className="card">
      <h2 className="card-name">{title}</h2>
      {children}
    </div>
  );
};

export default SectiopnCard;
