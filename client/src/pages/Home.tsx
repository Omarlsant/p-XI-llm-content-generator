import { Link } from 'react-router-dom';
import { AutoAwesome, Bolt, Group, Description } from '@mui/icons-material';
import Marquee from '../components/Marquee';
import TestimonialCarousel from '../components/TestimonialCarousel';

const Home = () => {
  return (
    <div className="space-y-24 py-16 pb-8">
      
      {/* --- HERO SECTION --- */}
      <section className="text-center px-4">
        <AutoAwesome className="text-cyan-300 mx-auto h-28 w-28 mb-4 drop-shadow-[0_0_15px_rgba(78,204,222,0.5)]" />
        <h1 className="text-5xl font-extrabold tracking-tight sm:text-6xl md:text-7xl bg-clip-text text-transparent bg-gradient-to-b from-slate-100 to-slate-400 py-2">
          Welcome to Post <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-violet-500">GenerAItor</span>
        </h1>
        <p className="mt-6 max-w-2xl mx-auto text-lg text-slate-400 sm:text-xl">
          Automate your content creation. Generate engaging posts for blogs, X, and Instagram with the power of AI. Save time and elevate your digital presence.
        </p>
        <div className="mt-10">
          <Link
            to="/generate"
            className="inline-block bg-gradient-to-r from-cyan-500 to-violet-600 text-white font-bold py-3 px-10 rounded-lg shadow-lg text-lg hover:shadow-xl hover:shadow-cyan-500/40 hover:-translate-y-1 transition-all duration-300"
          >
            Start Creating →
          </Link>
        </div>
      </section>

      {/* --- MARQUEE / LED TICKER SECTION --- */}
      <section>
        <Marquee />
      </section>

      {/* --- FEATURES SECTION --- */}
      <section className="max-w-5xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-12">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-8 text-center">
          {[
            { icon: <Bolt/>, title: "1. Define Your Topic", desc: "Simply enter the topic or idea you want to write about." },
            { icon: <Group/>, title: "2. Choose Platforms", desc: "Select the social media platforms or blog for which you need the content." },
            { icon: <Description/>, title: "3. Get Your Content", desc: "Our AI generates optimized text for each platform, ready to publish!" }
          ].map((feature, i) => (
            <div key={i} className="bg-slate-800/50 p-8 rounded-xl border border-slate-700 hover:border-cyan-500 transition-colors duration-300">
              <div className="text-cyan-400 h-12 w-12 mx-auto mb-5 flex items-center justify-center">{feature.icon}</div>
              <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
              <p className="text-slate-400">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* --- TESTIMONIAL CAROUSEL SECTION --- */}
      <section className="w-full">
        <h2 className="text-4xl font-bold text-center mb-12">What Our Users Say</h2>
        <TestimonialCarousel />
      </section>

      {/* --- FINAL CALL TO ACTION (CTA) SECTION --- */}
      <section className="max-w-4xl mx-auto px-4">
        <div className="p-1 rounded-xl bg-gradient-to-r from-cyan-500 to-violet-600">
          <div className="bg-slate-800/90 rounded-lg text-center p-10 md:p-16">
            <h2 className="text-3xl md:text-4xl font-extrabold bg-clip-text text-transparent bg-gradient-to-b from-slate-100 to-slate-400">
              Ready to Revolutionize Your Content?
            </h2>
            <p className="mt-4 text-lg text-slate-400 max-w-xl mx-auto">
              Stop staring at a blank page. Let AI be your creative partner and start producing high-quality content in a fraction of the time.
            </p>
            <div className="mt-8">
              <Link
                to="/generate"
                className="inline-block bg-gradient-to-r from-cyan-500 to-violet-600 text-white font-bold py-3 px-10 rounded-lg shadow-lg text-lg hover:shadow-xl hover:shadow-cyan-500/40 hover:-translate-y-1 transition-all duration-300"
              >
                Generate Your First Post
              </Link>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
};

export default Home;