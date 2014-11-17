import ycm_core
from os import getcwd, pardir, listdir
from os.path import abspath, join, isabs, normpath, exists, splitext, \
        dirname

##
# Some global lists
##

# This is the list of default flags.
default_flags = [
    "-Wall",
    "-Wextra"
]

# C header extensions
c_header_extensions = [
    ".h"
]

# C source extensions
c_source_extensions = [
    ".c"
]

# C additional flags
c_additional_flags = [
    # Tell clang that this is a C file.
    "-x",
    "c",

    # Use the latest standard if possible.
    "-std=c11"
]

# CPP header extensions
cpp_header_extensions = [
    ".h"
    ".hh",
    ".hpp",
    ".hxx"
]

# CPP source extensions
cpp_source_extensions = [
    ".cpp",
    ".cc",
    ".cxx"
]

# CPP additional flags
cpp_additional_flags = [
    # Tell clang that this file is a CPP file.
    "-x",
    "c++",

    # Use the latest standard if possible.
    "-std=c++11"
]


##
# Helper functions
##

# Methods to search for files in a file system tree.
def find_file_recursively(file_name, start_dir = getcwd()):
    """
    This method will walk trough the directory tree upwards
    starting at the given directory searching for a file with
    the given name.

    :param file_name: The name of the file of interest. Make sure
                      it does not contain any path information.
    :type file_name: str
    :param start_dir: The directory where the search should start.
                      If it is omitted, the cwd is used.
    :rtype: str
    :return: The file path where the file was first found.
    """
    cur_dir = abspath(start_dir) if not isabs(start_dir) else start_dir

    while True:
        if exists(join(cur_dir, file_name)):
            # The file of interest exists in the current directory
            # so return it.
            return join(cur_dir, file_name)

        # The file was not found yet so try in the parent directory.
        parent_dir = normpath(join(cur_dir, pardir))

        if parent_dir == cur_dir:
            # We are already at the base directory, so abort.
            return None
        else:
            cur_dir = parent_dir


def file_exists(file_name, start_dir = getcwd()):
    """
    Checks whether a file with the given file name exists in any parent
    folder of the given directory.

    :param file_name: The name of the file of interest.
    :type file_name: str
    :param start_dir: The directory where to start searching. If omitted the
                      cwd is used.
    :type start_dir: str
    :rtype: bool
    :return: True if the file was found or False if not.
    """
    return find_file_recursively(file_name, start_dir) is not None


# Methods to check whether a file is a header file.
def is_header(file_path):
    """
    Checks either the given file is a header file or not.

    :param file_path: The path to the file of interest.
    :type file_path: str
    :rtype: bool
    :return: True if the file is a header or False if not.
    """
    return is_c_header(file_path) or is_cpp_header(file_path)


def is_c_header(file_path):
    """
    Checks either the given file is a C header file or not.

    :param file_path: The path to the file of interest.
    :type file_path: str
    :rtype: bool
    :return: True if the file is a C header or False if not.
    """
    (_, extension) = splitext(file_path)

    return extension in c_header_extensions


def is_cpp_header(file_path):
    """
    Checks either the given file is a CPP header file or not.

    :param file_path: The path to the file of interest.
    :type file_path: str
    :rtype: bool
    :return: True if the file is a CPP header or False if not.
    """
    (_, extension) = splitext(file_path)

    return extension in cpp_header_extensions


# Methods to check whether a file is a source file.
def is_source(file_path):
    """
    Checks either the given file is a source file or not.

    :param file_path: The path to the file of interest.
    :type file_path: str
    :rtype: bool
    :return: True if the file is a source file or False if not.
    """
    return is_c_source(file_path) or is_cpp_source(file_path)


def is_c_source(file_path):
    """
    Checks either the given file is a C source file or not.

    :param file_path: The path to the file of interest.
    :type file_path: str
    :rtype: bool
    :return: True if the file is a C source file or False if not.
    """
    (_, extension) = splitext(file_path)

    return extension in c_source_extensions


def is_cpp_source(file_path):
    """
    Checks either the given file is a CPP source file or not.

    :param file_path: The path to the file of interest.
    :type file_path: str
    :rtype: bool
    :return: True if the file is a CPP source file or False if not.
    """
    (_, extension) = splitext(file_path)

    return extension in cpp_source_extensions


def is_c_file(file_path):
    """
    Checks if the given file is a C file or not.

    :param file_path: The path to the file of interest.
    :type file_path: str
    :rtype: bool
    :return: True if the file is a C file or False if not.
    """
    return is_c_source(file_path) or is_c_header(file_path)


def is_cpp_file(file_path):
    """
    Checks if the given file is a CPP file or not.

    :param file_path: The path to the file of interest.
    :type file_path: str
    :rtype: bool
    :return: True if the file is a CPP file or False if not.
    """
    return is_cpp_source(file_path) or is_cpp_header(file_path)


def make_path_absolute(path, base_dir=getcwd()):
    """
    Make a given path absolute using the given base directory if it is
    not already absolute.

    :param path: The path of interest.
    :type path: str
    :param base_dir: The directory which should be used to make the
                     path absolute. If it is omitted the cwd is used.
    :type base_dir: str
    :rtype: str
    :return: The absolute path.
    """
    if isabs(path):
        return path
    else:
        return join(base_dir, path)


def make_flags_absolute(flags, base_dir):
    """
    Makes all paths in the given flags which are relative absolute using
    the given base directory.

    :param flags: The list of flags which should be made absolute.
    :type flags: list[str]
    :param base_dir: The directory which should be used to make the relative
                     paths in the flags absolute.
    :type base_dir: str
    :rtype: list[str]
    :return: The list of flags with just absolute file paths.
    """
    # The list of flags which require a path as next flag.
    next_is_path = [
        "-I",
        "-isystem",
        "-iquote"
    ]

    # The list of flags which require a path as argument.
    argument_is_path = [
        "--sysroot="
    ]

    updated_flags = []
    make_absolute = False

    for flag in flags:
        updated_flag = flag

        if make_absolute:
            # Assume that the flag is a path.
            updated_flag = make_path_absolute(flag, base_dir)

            make_absolute = False

        # Check for flags which expect a path as next flag.
        if flag in next_is_path:
            # The flag following this one must be a path which may needs
            # to be made absolute.
            make_absolute = True

        # Check the flags which normally expect as the next flag a path,
        # but which are written in one string.
        for f in next_is_path:
            if flag.startswith(f):
                path = flag[len(f):].lstrip()

                # Split the flag up in two separate ones. One with the actual
                # flag and one with the path.
                updated_flags.append(f)
                updated_flag = make_path_absolute(path, base_dir)

                break

        for f in argument_is_path:
            if flag.startswith(f):
                path = flag[len(f):].lstrip()
                updated_flag = f + make_path_absolute(path, base_dir)

                break

        updated_flags.append(updated_flag)

    return updated_flags


def strip_flags(flags):
    """
    Remove leading and trailing spaces from the list of flags.

    :param flags: The list of flags which should be stripped.
    :type flags: list[str]
    :rtype: list[str]
    :return: The list of flags with leading and trailing spaces removed.
    """
    return [flag.strip() for flag in flags]


def script_directory():
    """
    Returns the directory where the current script is located.

    :rtype: str
    :return: The directory where the current script is located.
    """
    return dirname(__file__)


def make_flags_final(file_name, flags, base_dir = getcwd()):
    """
    Finalize the given flags for the file of interest. This step
    includes stripping the flags, making them absolute to the given
    base directory and adding the corresponding file type infos to them
    if necessary.

    :param file_name: The name of the file of interest.
    :type file_name: str
    :param flags: The flags which have been collected so far for the file.
    :type flags: list[str]
    :param base_dir: The directory which should be used to make the flags
                     absolute. If this is omitted the cwd is used.
    :type base_dir: str
    :rtype: dict[str,object]
    :return: The finalized flags for the file in the format wanted by YCM.
    """
    stripped = strip_flags(flags)
    absolute = make_flags_absolute(stripped, base_dir)

    if is_cpp_file(file_name):
        absolute.extend(cpp_additional_flags)
    elif is_c_file(file_name):
        absolute.extend(c_additional_flags)

    return create_result(absolute)


def create_result(flags, do_cache = True, **kwargs):
    """
    Create the correct return value for YCM.

    :param flags: The flags for the requested file.
    :type flags: list[str]
    :param do_cache: If the result should be cached by YCM or not. If this is
                     omitted True is used.
    :type do_cache: bool
    :param kwargs: Additional arguments.
    :type kwargs: dict[str,object]
    :rtype: dict[str,object]
    :return: A dictionary in the format wanted by YCM.
    """
    ret = {"flags": flags, "do_cache": do_cache}

    print(flags)

    return dict(ret, **kwargs)


def parse_compile_commands(file_name, search_base = getcwd()):
    """
    Parse the clang compile database generated by cmake. This database
    is normally saved by cmake in a file called "compile_commands.json".
    As we don't want to parse it on our own, functions provided by ycm_core
    are used. The flags corresponding to the file of interest are returned.
    If no information for this file could be found in the database, the
    default flags are used.

    :param file_name: The file for which flags should be created.
    :type file_name: str
    :param search_base: The directory at which the search for the database
                        file should start. If it is omitted the cwd is used.
    :rtype: dict[str,object]
    :returns: The flags found in the database in the format wanted by YCM.
    """
    database_path = dirname(find_file_recursively("compile_commands.json",
            search_base))

    database = ycm_core.CompilationDatabase(database_path)

    # As headers are not in the database, we have to use the corresponding
    # source file.
    if is_header(file_name):
        (name,_) = splitext(file_name)

        # Try out all C and CPP extensions for the corresponding source file.
        for ext in list(c_source_extensions, cpp_source_extensions):
            alternative_name = name + ext

            if exists(alternative_name):
                compilation_info = database.GetCompilationInfoForFile(alternative_name)

                # In the database we found flags for the alternative name
                if (compilation_info.compiler_flags_):
                    return make_flags_final(file_name, compilation_info.compiler_flags_,
                            compilation_info.compiler_working_dir_)

    elif is_source(file_name):
        compilation_info = database.GetCompilationInfoForFile(file_name)

        # We found flags for the file in the database
        if (compilation_info.compiler_flags_):
            return make_flags_final(file_name, compilation_info.compiler_flags_,
                    compilation_info.compiler_working_dir_)

    # We either don't have a proper file ending or did not find any information in the
    # database. Therefor use the default flags.
    return parse_default_flags(file_name)


def parse_clang_complete(file_name, search_base = getcwd()):
    """
    Parse the configuration file for the clang complete VIM plugin.
    Therefore it looks for a ".clang_complete" file starting at the
    given directory.

    :param file_name: The file for which flags should be created.
    :type file_name: str
    :param search_base: The directory where to start with the search for
                        the configuration file. If it is omitted the cwd is
                        used.
    :type search_base: str
    :rtype: dict[str,object]
    :returns: The flags found in the file in the format wanted by YCM.
    """
    config = find_file_recursively(".clang_complete", search_base)
    config_path = dirname(config)

    with open(config, "r") as config_file:
        flags = config_file.read().striplines()

        return make_flags_final(file_name, flags, config_path)


def parse_default_flags(file_name):
    """
    Parse and clean the default flags to use them as result for YCM.

    :param file_name: The file for which flags should be created.
    :type file_name: str
    :rtype: dict[str,object]
    :returns: The default flags in the format wanted by YCM.
    """
    return make_flags_final(file_name, default_flags, script_directory())


# The entry point in the file for the YCM VIM plugin.
def FlagsForFile(file_name, **kwargs):
    # First check for a compile_commands.json file.
    search_base = dirname(file_name)

    if file_exists("compile_commands.json", search_base):
        # There exists a compile_commands.json file. Try to use this one.
        return parse_compile_commands(file_name, search_base)
    elif file_exists(".clang_complete", search_base):
        # There exists a .clang_complete file. Try to use this one.
        return parse_clang_complete(file_name, search_base)
    else:
        # No files exists. Use the default flags.
        return parse_default_flags(file_name)

