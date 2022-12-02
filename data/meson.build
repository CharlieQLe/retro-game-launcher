desktop_file = i18n.merge_file(
        input: ('@0@.desktop.in').format(application_id),
       output: ('@0@.desktop').format(application_id),
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

appstream_file = i18n.merge_file(
        input: ('@0@.appdata.xml.in').format(application_id),
       output: ('@0@.appdata.xml').format(application_id),
       po_dir: '../po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util, args: ['validate', appstream_file])
endif

install_data(('@0@.gschema.xml').format(application_id),
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

install_subdir('presets',
  install_dir: pkgdatadir
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file',
       compile_schemas,
       args: ['--strict', '--dry-run', meson.current_source_dir()])
endif

subdir('icons')

blueprints = custom_target('blueprints',
  input: files(
    'ui/add_system_window.blp',
    'ui/dynamic_preferences_group.blp',
    'ui/game_view.blp',
    'ui/main_window.blp',
    'ui/minimal_window.blp',
    'ui/preferences.blp',
    'ui/system_box.blp',
    'ui/system_preferences.blp',
    'ui/system_row.blp',
    'ui/widgets/directory_entry_row.blp',
    'ui/widgets/game_item.blp',
    'ui/widgets/extension_row.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome = import('gnome')
gnome.compile_resources(application_id,
  ('@0@.gresource.xml').format(application_id),
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)