interface TechLogoProps {
  Icon: React.ElementType;
  name: string;
}

const TechLogo = ({ Icon, name }: TechLogoProps) => {
  return (
    <div className="flex flex-col items-center justify-center p-4 bg-slate-800 rounded-lg border border-slate-700 transition-all duration-300 hover:bg-slate-700/50 hover:border-cyan-500">
      <Icon className="h-12 w-12 mb-3 text-slate-300" />
      <p className="font-semibold text-slate-300">{name}</p>
    </div>
  );
};

export default TechLogo;