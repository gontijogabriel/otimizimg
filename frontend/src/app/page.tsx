import { type NextPage } from 'next';
import ImageUpload from "@/components/ImageUpload";

const Home: NextPage = () => {
    return (
        <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
                        Image Optimizer
                    </h1>
                    <p className="mt-3 text-xl text-gray-500 sm:mt-4">
                        Optimize your images in seconds
                    </p>
                </div>
                <ImageUpload />
            </div>
        </div>
    );
};

export default Home;