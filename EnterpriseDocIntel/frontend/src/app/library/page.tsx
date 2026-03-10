"use client";

import { useState } from "react";

const mockDocuments = [
  { id: "1", name: "Q3_Financial_Audit_Report.pdf", chunks: 452, date: "2023-10-15T09:30:00Z", size: "3.2 MB" },
  { id: "2", name: "Engineering_Architecture_v4.docx", chunks: 128, date: "2023-11-01T14:20:00Z", size: "1.1 MB" },
  { id: "3", name: "HR_Employee_Handbook_2024.pdf", chunks: 890, date: "2024-01-10T11:00:00Z", size: "5.4 MB" },
  { id: "4", name: "API_Security_Guidelines.txt", chunks: 45, date: "2024-02-05T16:45:00Z", size: "0.2 MB" },
];

export default function LibraryPage() {
  const [docs, setDocs] = useState(mockDocuments);

  const handleDelete = (id: string) => {
    if (confirm("Are you sure you want to remove this document and all its vector embeddings from ChromaDB?")) {
      setDocs(docs.filter(d => d.id !== id));
    }
  };

  return (
    <div className="flex flex-col gap-6 max-w-6xl">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-slate-900">Document Library</h2>
          <p className="text-sm text-slate-500 mt-1">Manage files currently indexed in the active vector database.</p>
        </div>
        
        <button className="text-sm text-red-600 bg-red-50 hover:bg-red-100 font-medium px-4 py-2 rounded-md transition-colors border border-red-200">
          Drop Index (Danger)
        </button>
      </div>

      <div className="bg-white border border-slate-200 shadow-sm rounded-xl overflow-hidden">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Document Name</th>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Indexed Chunks</th>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Upload Date</th>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Size</th>
              <th scope="col" className="relative px-6 py-4"><span className="sr-only">Actions</span></th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-slate-200">
            {docs.map((doc) => (
              <tr key={doc.id} className="hover:bg-slate-50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900 flex items-center gap-3">
                  <span className="text-lg">📄</span>
                  {doc.name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-800 border border-slate-200">
                    {doc.chunks} vectors
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                  {new Date(doc.date).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{doc.size}</td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button onClick={() => handleDelete(doc.id)} className="text-red-500 hover:text-red-700 hover:underline">Delete</button>
                </td>
              </tr>
            ))}
            
            {docs.length === 0 && (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-sm text-slate-500">
                  No documents found in the current index.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
