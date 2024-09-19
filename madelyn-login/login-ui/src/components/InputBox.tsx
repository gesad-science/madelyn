import React from "react";

interface InputBoxProps {
    type: string,
    placeholder: string,
    name: string
}

const InputBox: React.FC<InputBoxProps> = ( { type, placeholder, name } ) => {
  return (
    <div className="mb-6">
      <input
        type={type}
        placeholder={placeholder}
        name={name}
        className="w-full rounded-md border border-stroke px-5 py-3 text-base text-gray-950 focus:border-primary dark:border-dark-3"
      />
    </div>
  );
};

export default InputBox