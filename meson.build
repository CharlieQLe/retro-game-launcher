project('retro-game-launcher',
          version: '0.1.0',
    meson_version: '>= 0.59.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

project_id='retro-game-launcher'
application_id='com.charlieqle.RetroGameLauncher'

i18n = import('i18n')
gnome = import('gnome')
python = import('python')
pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())

subdir('data')
conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
conf.set('project_id', project_id)
conf.set('application_id', application_id)

message(project_id)

configure_file(
  input: ('@0@.in').format(project_id),
  output: project_id,
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

install_subdir(project_id.underscorify(), install_dir: pkgdatadir)

subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
