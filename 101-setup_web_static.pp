# Ensure /data directory exists with correct permissions
file { '/data':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Ensure /data/web_static directory structure exists with correct permissions
file { ['/data/web_static', '/data/web_static/releases', '/data/web_static/shared']:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Ensure /data/web_static/releases/test directory exists with correct permissions
file { '/data/web_static/releases/test':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create the fake HTML file with correct permissions
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  content => '<html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <p>This is a test page for web_static deployment.</p>
    </body>
</html>',
}

# Create symbolic link if it doesn't exist
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
}

# Notify service restart when the symbolic link changes
File['/data/web_static/current'] -> Service['nginx']

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => template('nginx/default.erb'),
}

service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
