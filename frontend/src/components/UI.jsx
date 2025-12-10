import { motion } from 'framer-motion';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export const GlassCard = ({ children, className, ...props }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className={twMerge("glass-panel rounded-2xl p-6", className)}
            {...props}
        >
            {children}
        </motion.div>
    );
};

export const Input = ({ label, ...props }) => {
    return (
        <div className="flex flex-col gap-2">
            {label && <label className="text-sm text-gray-400 font-medium">{label}</label>}
            <input
                className="input-glass rounded-xl px-4 py-3 w-full"
                {...props}
            />
        </div>
    );
};

export const Button = ({ children, className, variant = 'primary', ...props }) => {
    const variants = {
        primary: 'btn-ios',
        secondary: 'bg-white/10 text-white hover:bg-white/20',
        danger: 'bg-red-500 hover:bg-red-600 text-white'
    };

    return (
        <motion.button
            whileTap={{ scale: 0.98 }}
            className={twMerge("rounded-xl px-6 py-3 font-semibold transition-colors", variants[variant], className)}
            {...props}
        >
            {children}
        </motion.button>
    );
};
