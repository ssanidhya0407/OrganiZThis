import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { GlassCard, Input, Button } from '../components/UI';
import api from '../api/client';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Settings, LogOut, Database, User, Trash2 } from 'lucide-react';

export default function Dashboard() {
    const { user, logout } = useAuth();
    const [orgDetails, setOrgDetails] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [newName, setNewName] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetchOrgDetails();
    }, [user]);

    const fetchOrgDetails = async () => {
        if (!user?.organization_name) return;
        try {
            const res = await api.get('/org/get', { params: { organization_name: user.organization_name } });
            setOrgDetails(res.data);
            setNewName(res.data.organization_name);
        } catch (err) {
            console.error(err);
        }
    };

    const handleRename = async () => {
        try {
            await api.put('/org/update', { organization_name: newName });
            setMessage('Organization renamed successfully!');
            setIsEditing(false);

            // Update local storage
            localStorage.setItem('organization_name', newName); // Backend returns the new name in response actually, but we can trust input if successful? 
            // Ideally we use response data. 
            // But let's just use newName for simplicity as we checked it.

            // We must reload so AuthContext picks up new localStorage value?
            // Or we can expose a `updateUser` method in AuthContext.
            // For now, reloading is the "easiest" fix for the "stuck" state, IF we update localStorage FIRST.
            window.location.reload();
        } catch (err) {
            setMessage('Update failed: ' + (err.response?.data?.detail || err.message));
        }
    };

    const handleDelete = async () => {
        if (!window.confirm("Are you sure? This cannot be undone.")) return;
        try {
            await api.delete('/org/delete', { params: { organization_name: orgDetails.organization_name } });
            logout();
            navigate('/login');
        } catch (err) {
            setMessage('Delete failed: ' + (err.response?.data?.detail || err.message));
        }
    };

    if (!orgDetails) return <div className="text-center mt-20 text-gray-500">Loading...</div>;

    return (
        <div className="min-h-screen p-8 max-w-5xl mx-auto space-y-8">
            <header className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold">Dashboard</h2>
                    <p className="text-gray-400">Welcome, {user.email}</p>
                </div>
                <Button variant="secondary" onClick={() => { logout(); navigate('/login'); }}>
                    <LogOut size={18} className="mr-2 inline" /> Logout
                </Button>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <GlassCard className="col-span-1 md:col-span-2 space-y-6">
                    <div className="flex justify-between items-center">
                        <h3 className="text-xl font-semibold flex items-center gap-2">
                            <Database className="text-blue-500" /> Organization Details
                        </h3>
                        <Button variant="secondary" className="px-3 py-1 text-sm" onClick={() => setIsEditing(!isEditing)}>
                            <Settings size={14} className="mr-1 inline" /> {isEditing ? 'Cancel' : 'Edit'}
                        </Button>
                    </div>

                    <div className="space-y-4">
                        {isEditing ? (
                            <div className="flex gap-2 items-end">
                                <Input
                                    label="Organization Name"
                                    value={newName}
                                    onChange={(e) => setNewName(e.target.value)}
                                />
                                <Button onClick={handleRename}>Save</Button>
                            </div>
                        ) : (
                            <div>
                                <label className="text-sm text-gray-400">Organization Name</label>
                                <p className="text-2xl font-medium">{orgDetails.organization_name}</p>
                            </div>
                        )}

                        <div className="grid grid-cols-2 gap-4 pt-4 border-t border-white/10">
                            <div>
                                <label className="text-sm text-gray-400">Collection Name</label>
                                <code className="block bg-black/20 p-2 rounded-lg mt-1 text-sm text-green-400 font-mono">
                                    {orgDetails.collection_name}
                                </code>
                            </div>
                            <div>
                                <label className="text-sm text-gray-400">Admin Email</label>
                                <p className="text-white mt-2 flex items-center gap-2">
                                    <User size={16} /> {orgDetails.admin_email}
                                </p>
                            </div>
                        </div>
                    </div>

                    {message && <p className="text-yellow-400">{message}</p>}
                </GlassCard>

                <GlassCard className="col-span-1 bg-gradient-to-br from-red-500/10 to-orange-500/10 border-red-500/20">
                    <h3 className="text-xl font-semibold text-red-400 mb-4 flex items-center gap-2">
                        <Trash2 /> Danger Zone
                    </h3>
                    <p className="text-sm text-gray-400 mb-6">
                        Deleting the organization will remove all data permanently.
                    </p>
                    <Button variant="danger" className="w-full" onClick={handleDelete}>
                        Delete Organization
                    </Button>
                </GlassCard>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Placeholder Stats */}
                {[1, 2, 3, 4].map((i) => (
                    <GlassCard key={i} className="flex flex-col items-center justify-center py-8">
                        <span className="text-4xl font-bold text-white/20 mb-2">{i * 124}</span>
                        <span className="text-sm text-gray-500 uppercase tracking-widest">Active Records</span>
                    </GlassCard>
                ))}
            </div>
        </div>
    );
}
