"""
This file represents the EventGhost core/user plugins. The plugins can be obtained
by importing from eg.CorePluginModule/eg.UserPluginModule or by attribute name.
"""

import importlib.util
import sys
import eg
import os


class PluginModuleLoader(object):

    def __init__(self):
        mod = sys.modules.pop('eg.PluginModuleLoader')
        self.__dict__ = mod.__dict__
        self.__original_module__ = mod
        sys.modules[__name__] = self

    def __getattr__(self, module_name):
        if module_name in self.__dict__:
            return self.__dict__[module_name]

        if module_name in sys.modules:
            del sys.modules[module_name]

        file_path = os.path.join(self.__path__[0], module_name, '__init__.py')
        if not update_plugin_class(file_path):
            try:
                raise Exception(
                    'Plugin {0} needs to be manually updated'.format(module_name)
                )
            except Exception:
                import traceback
                eg.tl(traceback.format_exc())
            return False

        while True:
            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                self.__dict__[module_name] = module
                return module
            except RegisterPluginException:
                # It is expected that the loading will raise
                # RegisterPluginException because eg.RegisterPlugin() is called
                # inside the module
                if module_name in sys.modules:
                    del sys.modules[module_name]
                return True
            except:
                import traceback
                tb = traceback.format_exc()
                tb = tb.split('File')[-1]
                file_name = tb.split('"')[1]

                tb_path = os.path.split(file_name)[0]
                if module_name in sys.modules:
                    del sys.modules[module_name]

                if (
                    os.path.dirname(file_path) in tb_path
                    and find_errors(file_name)
                ):
                    continue
                else:
                    eg.tl(tb)
                    return False


class RegisterPluginException(Exception):
    """
    RegisterPlugin will raise this exception to interrupt the loading
    of the plugin module file.
    """
    pass


def update_plugin_class(file_name):
    backup_file = file_name + '.class.backup'

    with open(file_name, 'r', encoding='utf-8') as f:
        file_data = f.read()

    if '# super_class_updated' in file_data:
        return True

    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(file_data)

    file_data = file_data.splitlines()

    def has_parent_class():

        for parent_cls in (
            'eg.PluginBase',
            'eg.PluginClass',
            'eg.RawReceiverPlugin',
            'eg.IrDecoderPlugin'
        ):
            if parent_cls in line:
                return True
        return False

    cls_name = None
    cls_index = None
    init_index = None
    indent = None

    super_class_template = '{indent}super({cls_name}, self).__init__()'
    init_template = '{indent}def __init__(self):'
    for i, line in enumerate(file_data):
        if line.startswith('#'):
            continue

        if line.startswith('class'):
            if has_parent_class():
                cls_name = line.split(' ', 1)[1].split('(', 1)[0]
                eg.tl(cls_name)
                cls_index = i
                continue

        if cls_name is not None:
            if line.startswith('class') or line.startswith('def'):
                break

            if (
                indent is None and
                'def' in line and
                '(self' in line
            ):
                indent = line.split('def')[0]
                if '\t' in indent:
                    indent = '\t'
                else:
                    if indent not in ('    ', '  '):
                        indent = None

            if 'def __init__' in line:
                indent = line[:line.find('def')]
                init_index = True

            if init_index is True and line.strip().endswith('):'):
                init_index = i

            if 'super(' + cls_name in line:
                file_data.insert(1, '# super_class_updated')
                break

    if '# super_class_updated' not in file_data:
        if None in (indent, cls_name):
            return False

        if init_index is None:
            init_index = cls_index + 1
            template = init_template.format(indent=indent)
            file_data.insert(init_index, template)

        template = super_class_template.format(
            indent=indent * 2,
            cls_name=cls_name
        )
        file_data.insert(init_index + 1, template)
        file_data.insert(1, '# super_class_updated')

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('\n'.join(file_data))

    return True


def find_errors(file_name):
    import re
    replacements = (
        ('<>', '!='),
        (".decode('mbcs')", ''),
        ('.decode("mbcs")', ''),
        ("u'", "'"),
        ('u"', '"'),
        ('ur"', 'r"'),
        ("ur'", "r'"),
        ('iteritems()', 'items()'),
        ('itervalues()', 'values()'),
        ('iterkeys()', 'keys()')
    )

    with open(file_name, 'r', encoding='utf-8') as f:
        file_data = f.read()

    if '# update_complete' in file_data:
        return False

    backup_file = file_name + '.py3.backup'
    if os.path.exists(backup_file):
        with open(backup_file, 'r', encoding='utf-8') as f1:
            with open(file_name, 'w', encoding='utf-8') as f2:
                f2.write(f1.read())

        os.remove(backup_file)

    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(file_data)

    for pattern, replacement in replacements:
        file_data = file_data.replace(pattern, replacement)

    pattern = r'( |\(|,)0(\d+)'
    sub = r'\g<1>0o\2'

    file_data = re.sub(pattern, sub, file_data)

    patterns = [
        r'(\d)L(,|\)| |#)',
        r'(\d)l(,|\)| |#)',
        r'(\d)ul(,|\)| |#)',
        r'(\d)UL(,|\)| |#)'
    ]
    sub = r'\1\2'
    for pattern in patterns:
        file_data = re.sub(pattern, sub, file_data)

    lines = file_data.splitlines()
    offset = 0
    for i, line in enumerate(lines[:]):
        if line.strip().startswith('#'):
            continue

        if line.strip() == 'raise':
            indent = line[:line.find('raise')]
            line = line.replace(
                'raise',
                "raise Exception('Error in ' + frame.f_code.co_name)"
            )
            lines.insert(i, indent + 'frame = sys._getframe()')
            lines.insert(i, indent + 'import sys')
            offset += 2
        elif 'print ' in line:
            temp_line = line.strip()

            if 'pprint' in line and line.find('pprint') + 1 == line.find('print '):
                continue
            if temp_line.startswith('"') and temp_line.endswith('"'):
                continue
            if temp_line.startswith("'") and temp_line.endswith("'"):
                continue
            line = line.rstrip().replace('print ', 'print(') + ')'
        elif 'except ' in line:
            if ',' in line and '(' not in line and ')' not in line:
                line = line.replace(',', ' as ')
            elif ')' in line and ',' in line[line.find(')'):]:
                line_start = line[:line.find(')') + 1]
                line_end = line[line.find(')') + 1:]
                line_end = line_end.replace(',', ' as ', 1)
                line = line_start + line_end

        lines[i + offset] = line

    lines.insert(1, '# update_complete')

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return True
