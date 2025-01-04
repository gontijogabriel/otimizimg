'use client'
import React, { useState, ChangeEvent, DragEvent } from 'react';

interface ImageData {
    id: number;
    original_image: string;
    original_format: string;
    original_size: number;
    width: number;
    height: number;
    optimized_image?: string;
    optimized_format?: string;
    optimized_size?: number;
}

type ConversionFormat = 'WEBP' | 'JPEG' | 'PNG';

const ImageUpload: React.FC = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [imageData, setImageData] = useState<ImageData | null>(null);
    const [conversionFormat, setConversionFormat] = useState<ConversionFormat>('WEBP');
    const [isUploading, setIsUploading] = useState<boolean>(false);
    const [isOptimizing, setIsOptimizing] = useState<boolean>(false);
    const [error, setError] = useState<string>('');
    const [dragActive, setDragActive] = useState<boolean>(false);

    const handleDrag = (e: DragEvent<HTMLDivElement>): void => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e: DragEvent<HTMLDivElement>): void => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFiles(e.dataTransfer.files[0]);
        }
    };

    const handleFiles = (file: File): void => {
        if (file.type.startsWith('image/')) {
            setSelectedFile(file);
            setError('');
        } else {
            setError('Please select an image file');
        }
    };

    const handleFileInput = (e: ChangeEvent<HTMLInputElement>): void => {
        if (e.target.files && e.target.files[0]) {
            handleFiles(e.target.files[0]);
        }
    };

    const handleUpload = async (): Promise<void> => {
        if (!selectedFile) return;

        setIsUploading(true);
        setError('');
        const formData = new FormData();
        formData.append('original_image', selectedFile);

        try {
            const response = await fetch('http://localhost:8000/api/images/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Upload failed');

            const data = await response.json();
            setImageData(data);
        } catch (error) {
            setError('Failed to upload image. Please try again.');
        } finally {
            setIsUploading(false);
        }
    };

    const handleOptimization = async (): Promise<void> => {
        if (!imageData) return;

        setIsOptimizing(true);
        setError('');

        try {
            const response = await fetch(`http://localhost:8000/api/images/${imageData.id}/optimize/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    format: conversionFormat,
                    quality: 85,
                }),
            });

            if (!response.ok) throw new Error('Optimization failed');

            const data = await response.json();
            console.log(JSON.stringify(data, null, 2))
            setImageData(data);
        } catch (error) {
            setError('Failed to optimize image. Please try again.');
        } finally {
            setIsOptimizing(false);
        }
    };

    const formatBytes = (bytes: number): string => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    return (
        <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
            {error && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-600 rounded-lg">
                    {error}
                </div>
            )}

            <div
                className={`relative border-2 border-dashed rounded-lg p-8 text-center mb-6 transition-colors
          ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
          ${selectedFile ? 'bg-gray-50' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <input
                    type="file"
                    onChange={handleFileInput}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    accept="image/*"
                />
                <div className="space-y-2">
                    {selectedFile ? (
                        <div className="text-gray-600">
                            Selected: {selectedFile.name}
                        </div>
                    ) : (
                        <>
                            <p className="text-gray-600">Drag and drop your image here or click to select</p>
                            <p className="text-sm text-gray-500">Supports: JPG, PNG, WebP</p>
                        </>
                    )}
                </div>
            </div>

            {selectedFile && !imageData && (
                <button
                    onClick={handleUpload}
                    disabled={isUploading}
                    className={`w-full py-2 px-4 rounded-lg text-white transition-colors
            ${isUploading ? 'bg-blue-400' : 'bg-blue-600 hover:bg-blue-700'}`}
                >
                    {isUploading ? 'Uploading...' : 'Upload Image'}
                </button>
            )}

            {imageData && (
                <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="space-y-4">
                            <h3 className="text-lg font-semibold">Original Image</h3>
                            <img
                                src={`http://localhost:8000/${imageData.original_image}`}
                                alt="Original"
                                className="w-full rounded-lg shadow"
                            />
                            <div className="text-sm text-gray-600 space-y-1">
                                <p>Format: {imageData.original_format}</p>
                                <p>Size: {formatBytes(imageData.original_size)}</p>
                                <p>Dimensions: {imageData.width} x {imageData.height}</p>
                            </div>
                        </div>

                        {imageData.optimized_image && (
                            <div className="space-y-4">
                                <h3 className="text-lg font-semibold">Optimized Image</h3>
                                <img
                                    src={`${imageData.optimized_image}`}
                                    alt="Optimized"
                                    className="w-full rounded-lg shadow"
                                />
                                <div className="text-sm text-gray-600 space-y-1">
                                    <p>Format: {imageData.optimized_format}</p>
                                    <p>Size: {formatBytes(imageData.optimized_size || 0)}</p>
                                    <p>Savings: {imageData.optimized_size ? (100 - (imageData.optimized_size / imageData.original_size * 100)).toFixed(1) : 0}%</p>
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="border-t pt-6">
                        <div className="flex flex-col sm:flex-row gap-4">
                            <select
                                value={conversionFormat}
                                onChange={(e) => setConversionFormat(e.target.value as ConversionFormat)}
                                className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="WEBP">WebP (Recommended)</option>
                                <option value="JPEG">JPEG</option>
                                <option value="PNG">PNG</option>
                            </select>

                            <button
                                onClick={handleOptimization}
                                disabled={isOptimizing}
                                className={`flex-1 py-2 px-4 rounded-lg text-white transition-colors
                  ${isOptimizing ? 'bg-green-400' : 'bg-green-600 hover:bg-green-700'}`}
                            >
                                {isOptimizing ? 'Optimizing...' : 'Optimize Image'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ImageUpload;