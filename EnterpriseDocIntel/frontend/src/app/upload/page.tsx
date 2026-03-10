"use client";

import { useState } from "react";
import axios from "axios";

export default function UploadPage() {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [chunkSize, setChunkSize] = useState(1000);
  const [chunkOverlap, setChunkOverlap] = useState(200);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    
    const formData = new FormData();
    formData.append("file", file);
    formData.append("chunk_size", chunkSize.toString());
    formData.append("chunk_overlap", chunkOverlap.toString());

    try {
      const response = await axios.post("http://localhost:8000/api/v1/docs/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
      alert(`Success: ${response.data.message}`);
      setFile(null);
    } catch (error: any) {
      console.error(error);
      alert(`Error: ${error.response?.data?.detail || "Failed to upload document"}`);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6 max-w-4xl">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-slate-900">Upload Documents</h2>
        <p className="text-sm text-slate-500 mt-1">Ingest new PDFs, TXTs, or DOCXs into the enterprise vector baseline.</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
        <div
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
            isDragging ? "border-emerald-500 bg-emerald-50" : "border-slate-300 bg-slate-50"
          }`}
        >
          <div className="text-4xl mb-4">📄</div>
          {file ? (
             <div className="flex flex-col items-center">
               <p className="text-sm font-medium text-slate-900">{file.name}</p>
               <p className="text-xs text-slate-500 mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
               <button onClick={() => setFile(null)} className="text-xs text-red-500 mt-4 hover:underline">Remove file</button>
             </div>
          ) : (
            <>
              <p className="text-sm font-medium text-slate-700">Drag and drop a file here, or click to browse</p>
              <p className="text-xs text-slate-400 mt-2">Supports PDF, DOCX, TXT. Max size 20MB.</p>
              <input type="file" className="hidden" id="file-upload" onChange={(e) => e.target.files && setFile(e.target.files[0])} />
              <label htmlFor="file-upload" className="mt-6 inline-flex cursor-pointer items-center px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50">
                Select File
              </label>
            </>
          )}
        </div>

        {file && (
          <div className="mt-8">
            <h3 className="text-sm font-bold text-slate-900 mb-4 border-b pb-2">Embedding Configuration</h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1 flex items-center gap-1 cursor-help relative group">
                  Chunk Size (Words) ℹ
                  <div className="absolute top-6 left-0 w-48 p-2 bg-slate-800 text-slate-100 text-xs rounded opacity-0 group-hover:opacity-100 pointer-events-none z-50">
                    How many words per embedded segment. Larger sizes capture more context but dilute precision.
                  </div>
                </label>
                <input 
                  type="number" 
                  value={chunkSize}
                  onChange={(e) => setChunkSize(parseInt(e.target.value))}
                  className="w-full text-sm border-slate-300 rounded-md shadow-sm focus:ring-emerald-500 focus:border-emerald-500" 
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1 flex items-center gap-1 cursor-help relative group">
                  Chunk Overlap ℹ
                  <div className="absolute top-6 left-0 w-48 p-2 bg-slate-800 text-slate-100 text-xs rounded opacity-0 group-hover:opacity-100 pointer-events-none z-50">
                    Overlap prevents vital sentences from being cut in half at chunk boundaries.
                  </div>
                </label>
                <input 
                  type="number" 
                  value={chunkOverlap}
                  onChange={(e) => setChunkOverlap(parseInt(e.target.value))}
                  className="w-full text-sm border-slate-300 rounded-md shadow-sm focus:ring-emerald-500 focus:border-emerald-500" 
                />
              </div>
            </div>

            <div className="mt-8 flex justify-end">
               <button
                 onClick={handleUpload}
                 disabled={isUploading}
                 className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white font-medium rounded-md text-sm px-6 py-2.5 transition-colors disabled:opacity-50"
               >
                 {isUploading ? <div className="w-4 h-4 rounded-full border-2 border-white/50 border-t-white animate-spin"/> : "Start Embedding Pipeline"}
               </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
